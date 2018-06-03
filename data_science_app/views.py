import os
from django.core.files import File
from rest_framework.response import Response

from data_science_app.serializers import UserSerializer, AnalysisSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from data_science_app.permissions import IsOwnerOrReadOnly
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions, status
from django.conf import settings
from data_science_app.forms import UserFormEdit
from django.http import HttpResponse, Http404
from rest_framework.decorators import action
from data_science_app.models import Analysis
from django.contrib.auth.models import User
from ds_class.ds_execute import WebDataScienceExecute
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

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
            execute = WebDataScienceExecute(analysis)
            execute.execute()
            return redirect(reverse_lazy('desktop'))
        else:
            raise PermissionDenied


class SearchView(generic.ListView):
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        founded = Analysis.objects.filter((Q(name__icontains=query) | Q(ws__icontains=query) | Q(
            wd__icontains=query) | Q(date_create__icontains=query) | Q(date_modified__icontains=query)) & Q(
            user=self.request.user))

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


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @action(detail=True)
    def execute(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            try:
                execute = WebDataScienceExecute(analysis)
                execute.execute()
                return Response({}, status=status.HTTP_200_OK)
            except:
                raise Http404
        raise PermissionDenied

    @action(methods=['post'], detail=True)
    def load_file_data(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            try:
                file_name = request.data['file_path']
                file_data = File(open(file_name, 'r'))
                analysis.file_data.save (f'{analysis.name}.csv', file_data, save=True)
                file_data.close()
                return Response({}, status=status.HTTP_200_OK)
            except:
                raise Http404
        raise PermissionDenied

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            if analysis.file_zip != "":
                response = HttpResponse(analysis.file_zip)
                response["Content-Disposition"] = 'attachment; filename="{}.zip"'.format(analysis.name)
                return response
            raise Http404
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
