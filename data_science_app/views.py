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
from data_science_app.models import Analise
from ds_class.calculate import Calculate
from ds_class.df_filter import DfFilter
from ds_class.df_group import DfGroup
from ds_class.graphs import Graphs

DEFAULT_LOGIN_URL = '/sign_in'


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
            my_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=my_password)
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
    template_name = "desktop_analises.html"
    model = Analise
    context_object_name = "analises"

    def get_queryset(self):
        return Analise.objects.all()


class Details(generic.DetailView):
    template_name = "details.html"
    model = Analise

    def get_object(self, queryset=None):
        obj = super(Details, self).get_object(queryset=queryset)
        return obj

    def get_queryset(self):
        queryset = super(Details, self).get_queryset()
        return queryset.filter(user=self.request.user)


class NewAnalysis(generic.CreateView):
    template_name = "new_analise.html"
    model = Analise
    fields = ('name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'File_Data')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(reverse_lazy('desktop'))


class EditAnalysis(generic.UpdateView):
    template_name = "edit_analise.html"
    model = Analise
    fields = ('name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'File_Data')
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = super(EditAnalysis, self).get_object(queryset=queryset)
        return obj

    def get_queryset(self):
        queryset = super(EditAnalysis, self).get_queryset()
        return queryset.filter(user=self.request.user)


class DeleteAnalysis(generic.DeleteView):
    template_name = "analise_confirm_delete.html"
    model = Analise
    success_url = reverse_lazy('desktop')

    def get_object(self, queryset=None):
        obj = super(DeleteAnalysis, self).get_object(queryset=queryset)
        return obj

    def get_queryset(self):
        queryset = super(DeleteAnalysis, self).get_queryset()
        return queryset.filter(user=self.request.user)


class DoAnalysis(generic.View):
    template_name = "Analize.html"
    model = Analise
    context_object_name = "analise"

    def get(self, request, *args, **kwargs):
        analise = Analise.objects.get(id=kwargs['pk'])
        if analise.user == request.user:
            output_dir = os.path.join(settings.MEDIA_ROOT, analise.name)
            download_dir = os.path.join(settings.MEDIA_ROOT, "downloads")

            self.create_dirs(output_dir, download_dir)
            self.data_science_execute(analise, output_dir)
            self.packing_zip(output_dir, download_dir, analise.name)

            zip_pack_file = os.path.join(download_dir, f'{analise.name}_pack.zip')
            zip_pack = File(open(zip_pack_file, 'rb'))
            analise.File_Zip.save(f'{analise.name}.zip', zip_pack, save=True)
            zip_pack.close()

            if os.path.exists(zip_pack_file):
                os.remove(zip_pack_file)

            return render(request, self.template_name, {'done': True})
        else:
            return render(request, self.template_name, {'done': False})

    @staticmethod
    def create_dirs(*dirs):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    @staticmethod
    def data_science_execute(analise, output_dir):
        df = DfFilter(pd.read_csv(analise.File_Data.path, sep=';', index_col="Timestamp"))

        df.first_filter()
        df.general_filter(analise.WS, analise.WS_Start, analise.WS_Stop)
        df.general_filter(analise.WD, analise.WD_Start, analise.WD_Stop)
        df.df_filtered["AD_1"] = Calculate.ad(df.df_filtered)
        filtered_file = "{}_filtered.csv".format(analise.name)

        pd.DataFrame.to_csv(df.df_filtered, os.path.join(output_dir, filtered_file))
        df_group = DfGroup(df.df_filtered)
        df_group.group_df(analise.WD, analise.WD_Start, analise.WD_Stop, analise.WD_Step)
        df_group.df_grouped = df_group.df_grouped.mean()
        group_file = "{}_group.csv".format(analise.name)

        pd.DataFrame.to_csv(df_group.df_grouped, os.path.join(output_dir, group_file))

        graph = Graphs(df.df_filtered, df_group.df_grouped)
        graph.wind_rose(analise.WD, analise.WD_Step, os.path.join(output_dir, '{}_wd_rose.png'.format(analise.name)))
        graph.hist(analise.WS, os.path.join(output_dir, '{}_hist.png'.format(analise.name)))
        graph.time("AD_1", os.path.join(output_dir, '{}_time.png'.format(analise.name)))
        graph.ws_wd(analise.WD, analise.WS, os.path.join(output_dir, '{}_ws_wd.png'.format(analise.name)))

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
            founded = Analise.objects.filter(
                Q(name__icontains=query) | Q(WS__icontains=query) | Q(WD__icontains=query) |
                Q(Date_Create__icontains=query) | Q(Date_Modified__icontains=query))
            print(founded)
            context['last_query'] = query
            context['user'] = request.user
            context['analysis_list'] = founded
        return render(request, self.template_name, context)


class DownloadZip(generic.View):

    def get(self, request, *args, **kwargs):
        analise = Analise.objects.get(id=kwargs['pk'])
        if analise.user == request.user:
            if analise.File_Zip == "":
                response = HttpResponse(analise.File_Zip)
                response["Content-Disposition"] = 'attachment; filename="{}.zip"'.format(analise.name)
                return response
            else:
                return redirect(reverse_lazy('desktop'))

        else:
            return render(request, "Analize.html", {'done': False})
