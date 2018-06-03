from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from rest_framework.views import APIView

from data_science_app.serializers import UserSerializer, AnalysisSerializer
from django.core.exceptions import PermissionDenied
from data_science_app.forms import UserFormEdit
from data_science_app.models import Analysis
from ds_class.ds_class import DataScienceRun
from django.contrib.auth.models import User
from django.views import View, generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.files import File
from django.conf import settings
from django.db.models import Q
from django.http import Http404
import zipfile
import shutil
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


PAGINATION_PAGES = 4


class SignUp(generic.CreateView):
    template_name = "sign_up.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("user")


class UserEdit(generic.UpdateView):
    model = User
    form_class = UserFormEdit
    template_name = "user.html"
    success_url = reverse_lazy("desktop")

    def get_object(self, queryset=None):
        return self.request.user


class Desktop(generic.ListView):
    template_name = "desktop.html"
    model = Analysis
    context_object_name = "analyses"
    queryset = Analysis.objects.all()

    def get_queryset(self):
        queryset = super(Desktop, self).get_queryset()
        paginator = Paginator(queryset.filter(user=self.request.user), PAGINATION_PAGES)
        page = self.request.GET.get('page')
        try:
            analyses = paginator.page(page)
        except PageNotAnInteger:
            analyses = paginator.page(1)
        except EmptyPage:
            analyses = paginator.page(paginator.num_pages)
        return analyses

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context['analyses'] = self.get_queryset()
        return context


class Details(generic.DetailView):
    template_name = "details.html"
    model = Analysis

    def get_object(self, queryset=None):
        obj = super(Details, self).get_object(queryset=queryset)
        return obj

    def get_queryset(self):
        queryset = super(Details, self).get_queryset()
        return queryset.filter(user=self.request.user)


class NewAnalysis(generic.CreateView):
    template_name = "new_analysis.html"
    model = Analysis
    fields = ('name', 'ws', 'wd', 'wd_step', 'wd_start', 'wd_stop', 'ws_start', 'ws_stop', 'file_data')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(reverse_lazy('desktop'))


class EditAnalysis(generic.UpdateView):
    template_name = "edit_analysis.html"
    model = Analysis
    fields = ('name', 'ws', 'wd', 'wd_step', 'wd_start', 'wd_stop', 'ws_start', 'ws_stop', 'file_data')
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = super(EditAnalysis, self).get_object(queryset=queryset)
        return obj or Http404

    def get_queryset(self):
        queryset = super(EditAnalysis, self).get_queryset()
        return queryset.filter(user=self.request.user)


class DeleteAnalysis(generic.DeleteView):
    template_name = "delete.html"
    model = Analysis
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = super(DeleteAnalysis, self).get_object(queryset=queryset)
        return obj

    def get_queryset(self):
        queryset = super(DeleteAnalysis, self).get_queryset()
        return queryset.filter(user=self.request.user)


class AnalysisExecute(generic.RedirectView):
    model = Analysis
    context_object_name = "analysis"

    def get(self, request, *args, **kwargs):
        analysis = Analysis.objects.get(id=kwargs['pk'])
        if analysis.user == request.user:
            output_dir = os.path.join(settings.MEDIA_ROOT, analysis.name)
            download_dir = os.path.join(settings.MEDIA_ROOT, "downloads")

            self.create_dirs(output_dir, download_dir)

            analysis_dict = analysis.__dict__
            analysis_dict['file_data'] = analysis.file_data.path

            ds_runner = DataScienceRun(analysis_dict, output_dir)
            ds_runner.data_science_execute()

            self.packing_zip(output_dir, download_dir, analysis.name)
            zip_pack_file = os.path.join(download_dir, f'{analysis.name}_pack.zip')

            zip_pack = File(open(zip_pack_file, 'rb'))
            analysis.file_zip.save(f'{analysis.name}.zip', zip_pack, save=True)
            zip_pack.close()

            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, analysis.name))

            if os.path.exists(zip_pack_file):
                os.remove(zip_pack_file)
            return redirect(reverse_lazy('desktop'))
        else:
            raise PermissionDenied

    @staticmethod
    def create_dirs(*dirs):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    @staticmethod
    def packing_zip(from_dir, to_dir, name_zip):
        if os.path.exists(os.path.join(to_dir, f'{name_zip}.zip')):
            os.remove(os.path.join(to_dir, f'{name_zip}.zip'))
        if os.path.exists(os.path.join(to_dir, f'{name_zip}_pack.zip')):
            os.remove(os.path.join(to_dir, f'{name_zip}_pack.zip'))

        file_name = os.path.join(to_dir, f'{name_zip}_pack.zip')
        zip_archive = zipfile.ZipFile(file_name, "w")
        for file in os.listdir(from_dir):
            print(os.path.join(from_dir, file))
            zip_archive.write(os.path.join(from_dir, file), file)
        zip_archive.close()
        return zip_archive


class SearchView(generic.ListView):
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        founded = Analysis.objects.filter((
                                                  Q(name__icontains=query) | Q(ws__icontains=query) | Q(
                                              wd__icontains=query) |
                                                  Q(date_create__icontains=query) | Q(
                                              date_modified__icontains=query)) & Q(user=self.request.user))

        paginator = Paginator(founded, PAGINATION_PAGES)
        page = self.request.GET.get('page')
        try:
            founded = paginator.page(page)
        except PageNotAnInteger:
            founded = paginator.page(1)
        except EmptyPage:
            founded = paginator.page(paginator.num_pages)
        return founded

    def get_context_data(self, *, object_list=None, **kwargs):

        context = {}
        query = self.request.GET.get('q')
        context['last_query'] = query
        context['user'] = self.request.user
        context['analysis_list'] = self.get_queryset()
        return context


class DownloadZip(generic.View):

    def get(self, request, *args, **kwargs):
        try:
            analysis = get_object_or_404(Analysis, pk=kwargs['pk'])
            if analysis.user == request.user:
                if analysis.file_zip != "":
                    response = HttpResponse(analysis.file_zip)
                    response["Content-Disposition"] = 'attachment; filename="{}.zip"'.format(analysis.name)
                    return response
            else:
                raise PermissionDenied
        except:
            raise Http404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class AnalysesViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer


class AnalysisList(APIView):
    def get(self, request):
        analyses = Analysis.objects.all()
        serializer = AnalysisSerializer(analyses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Analysis.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        analysis = self.get_object(pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        analysis = self.get_object(pk)
        serializer = AnalysisSerializer(analysis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        analysis = self.get_object(pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def analysis_list(request):
    if request.method == 'GET':
        analyses = Analysis.objects.all()
        serializer = AnalysisSerializer(analyses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def analysis_detail(request, pk):
    try:
        analysis = Analysis.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AnalysisSerializer(analysis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)