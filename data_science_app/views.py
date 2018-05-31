import os
import zipfile
import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from data_science_app.forms import UserFormEdit
from data_science_app.models import Analysis
from ds_class.calculate import Calculate
from ds_class.df_filter import DfFilter
from ds_class.df_group import DfGroup
from ds_class.graphs import Graphs


class SignUp(View):
    template_name = "sign_up.html"

    def get(self, request):
        user_form = UserCreationForm()
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse_lazy("user"))
        return redirect(reverse_lazy("sign_up"))


class UserEdit(View):
    template_name = "user.html"

    def get(self, request):
        user_form = UserFormEdit(instance=request.user)
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request):
        user_form = UserFormEdit(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse_lazy("desktop"))
        return redirect(reverse_lazy("user"))


class Desktop(generic.ListView):
    template_name = "desktop.html"
    model = Analysis
    context_object_name = "analyses"

    def get_queryset(self):
        return Analysis.objects.all()


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
        return obj

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


class AnalysisExecute(generic.View):
    template_name = "info.html"
    model = Analysis
    context_object_name = "analysis"

    def get(self, request, *args, **kwargs):
        context = {}
        context['mode'] = 'execute'
        analysis = Analysis.objects.get(id=kwargs['pk'])
        if analysis.user == request.user:
            output_dir = os.path.join(settings.MEDIA_ROOT, analysis.name)
            download_dir = os.path.join(settings.MEDIA_ROOT, "downloads")

            self.create_dirs(output_dir, download_dir)
            self.data_science_execute(analysis, output_dir)
            self.packing_zip(output_dir, download_dir, analysis.name)

            zip_pack_file = os.path.join(download_dir, f'{analysis.name}_pack.zip')
            zip_pack = File(open(zip_pack_file, 'rb'))
            analysis.file_zip.save(f'{analysis.name}.zip', zip_pack, save=True)
            zip_pack.close()

            if os.path.exists(zip_pack_file):
                os.remove(zip_pack_file)

            context['success'] = True

            return render(request, self.template_name, context)
        else:
            context['success'] = False
            return render(request, self.template_name, context)

    @staticmethod
    def create_dirs(*dirs):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    @staticmethod
    def data_science_execute(analysis, output_dir):
        df = DfFilter(pd.read_csv(analysis.file_data.path, sep=';', index_col="Timestamp"))

        df.first_filter()
        df.general_filter(analysis.ws, analysis.ws_start, analysis.ws_stop)
        df.general_filter(analysis.wd, analysis.wd_start, analysis.wd_stop)
        df.df_filtered["AD_1"] = Calculate.ad(df.df_filtered)
        filtered_file = "{}_filtered.csv".format(analysis.name)

        pd.DataFrame.to_csv(df.df_filtered, os.path.join(output_dir, filtered_file))
        df_group = DfGroup(df.df_filtered)
        df_group.group_df(analysis.wd, analysis.wd_start, analysis.wd_stop, analysis.wd_step)
        df_group.df_grouped = df_group.df_grouped.mean()
        group_file = "{}_group.csv".format(analysis.name)

        pd.DataFrame.to_csv(df_group.df_grouped, os.path.join(output_dir, group_file))

        graph = Graphs(df.df_filtered, df_group.df_grouped)
        graph.wind_rose(analysis.wd, analysis.wd_step, os.path.join(output_dir, '{}_wd_rose.png'.format(analysis.name)))
        graph.hist(analysis.ws, os.path.join(output_dir, '{}_hist.png'.format(analysis.name)))
        graph.time("AD_1", os.path.join(output_dir, '{}_time.png'.format(analysis.name)))
        graph.ws_wd(analysis.wd, analysis.ws, os.path.join(output_dir, '{}_ws_wd.png'.format(analysis.name)))

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


class SearchView(generic.View):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        context = {}
        query = request.GET.get('q')
        if query is not None:
            founded = Analysis.objects.filter(
                Q(name__icontains=query) | Q(ws__icontains=query) | Q(wd__icontains=query) |
                Q(date_create__icontains=query) | Q(date_modified__icontains=query))
            print(founded)
            context['last_query'] = query
            context['user'] = request.user
            context['analysis_list'] = founded
        return render(request, self.template_name, context)


class DownloadZip(generic.View):
    def get(self, request, *args, **kwargs):
        analysis = Analysis.objects.get(id=kwargs['pk'])
        if analysis.user == request.user:
            if analysis.file_zip != "":
                response = HttpResponse(analysis.file_zip)
                response["Content-Disposition"] = 'attachment; filename="{}.zip"'.format(analysis.name)
                return response
            else:
                return redirect(reverse_lazy('desktop'))
        else:
            context = {}
            context['mode'] = 'no_access'
            return render(request, "info.html", context)
