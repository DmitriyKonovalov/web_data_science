import os

import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View, generic
from data_science_app.forms import UserFormEdit
from data_science_app.models import Analise
from ds_class.calculate import Calculate
from ds_class.df_filter import DfFilter
from ds_class.df_group import DfGroup
from ds_class.graphs import Graphs

DEFAULT_LOGIN_URL = '/sign_in'


@login_required(login_url=DEFAULT_LOGIN_URL)
def home(request):
    return render(request, 'home.html', {})


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
            return redirect(home)
        return redirect(reverse_lazy("user"))


class Desktop(generic.ListView):
    template_name = "desktop_analises.html"
    model = Analise
    context_object_name = "analises"

    def get_queryset(self):
        return Analise.objects.all()


class Details(generic.ListView):
    template_name = "details.html"
    model = Analise
    context_object_name = "analise"

    def get_queryset(self):
        return Analise.objects.get(id=self.kwargs['pk'])


class NewAnalysis(generic.CreateView):
    template_name = "new_analise.html"
    model = Analise
    fields = ('name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'File_Data')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.Date_Create = now()
        obj.Date_Modified = now()
        obj.save()
        return redirect(reverse_lazy('desktop'))


class EditAnalysis(generic.UpdateView):
    template_name = "edit_analise.html"
    model = Analise
    fields = ('name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'File_Data')
    success_url = reverse_lazy('desktop')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Date_Modified = now()
        obj.save()
        return redirect(self.success_url)

class DeleteAnalysis(generic.DeleteView):
    template_name = "analise_confirm_delete.html"
    model = Analise
    fields = ('name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'File_Data')
    success_url = reverse_lazy('desktop')


class DoAnalysis(generic.View):
    template_name = "Analize.html"
    model = Analise
    context_object_name = "analise"

    def get(self, request, *args, **kwargs):
        analise = Analise.objects.get(id=kwargs['pk'])

        df = DfFilter(pd.read_csv(analise.File_Data.path, sep=';', index_col="Timestamp"))
        df.first_filter()
        df.general_filter(analise.WS, analise.WS_Start, analise.WS_Stop)
        df.general_filter(analise.WD, analise.WD_Start, analise.WD_Stop)
        df.df_filtered["AD_1"] = Calculate.ad(df.df_filtered)

        output_dir = os.path.join(settings.MEDIA_ROOT, analise.name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

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
        return render(request, self.template_name, {})
