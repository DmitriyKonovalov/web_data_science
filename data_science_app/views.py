from django.shortcuts import render, redirect
from data_science_app.models import Analise
from data_science_app.forms import New_Analise_Form, User_Form, User_Form_Edit, Edit_Analise_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ds_class.calculate import Calculate
from ds_class.df_filter import DfFilter
from ds_class.df_group import DfGroup
from ds_class.graphs import Graphs
import pandas as pd
from django.conf import settings
import os

DEFAULT_LOGIN_URL='/sign_in'

@login_required(login_url=DEFAULT_LOGIN_URL)
def home(request):
    return render(request,'home.html', {})

# Убрать
def sign_up(request):
    user_form = User_Form()
    if request.method == "POST":
        user_form=User_Form(request.POST)
    if user_form.is_valid():
        new_user = User.objects.create_user(**user_form.cleaned_data)
        user = authenticate(
            username = user_form.cleaned_data['username'],
            password = user_form.cleaned_data['password']
        )
        login(request,user)
        return redirect(home)
    return render(request, 'sign_up.html', {'user_form': user_form})


@login_required(login_url=DEFAULT_LOGIN_URL)
def desktop(request):
    analises = Analise.objects.all()
    return render(request,'desktop_analises.html', {'analises': analises, 'user': request.user})


@login_required(login_url=DEFAULT_LOGIN_URL)
def view_new_analise(request):
    form = New_Analise_Form()
    if request.method == 'POST':
        form = New_Analise_Form(request.POST or None, files=request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            return redirect(desktop)
    return render(request, 'new_analise.html', {'form': form})

@login_required(login_url=DEFAULT_LOGIN_URL)
def view_detail(request,analise_id):
    analise = Analise.objects.get(id = analise_id)
    return render(request, 'details.html', {'analise': analise, 'user': request.user})


@login_required(login_url=DEFAULT_LOGIN_URL)
def user_edit(request):
    user_form = User_Form_Edit(instance=request.user)
    if request.method == 'POST':
        user_form = User_Form_Edit(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(home)
    return render(request, 'user.html', {'user_form': user_form})


@login_required(login_url=DEFAULT_LOGIN_URL)
def edit_analise(request,analise_id):
    analise_form = Edit_Analise_Form(instance = Analise.objects.get(id = analise_id))
    if request.method == 'POST':
        analise_form= Edit_Analise_Form(request.POST, request.FILES, instance=Analise.objects.get(id=analise_id))
        if analise_form.is_valid():
            analise_form.save()
    return render(request, 'edit_analise.html', {'form': analise_form, 'analise_id':analise_id})


@login_required(login_url=DEFAULT_LOGIN_URL)
def _analize(request,analise_id):
    analise=Analise.objects.get(id = analise_id)

    df = DfFilter(pd.read_csv(analise.File_Data.path, sep=';', index_col="Timestamp"))

    df.first_filter()
    df.general_filter(analise.WS, analise.WS_Start, analise.WS_Stop)
    df.general_filter(analise.WD, analise.WD_Start, analise.WD_Stop)
    df.df_filtered["AD_1"] = Calculate.ad(df.df_filtered)

    output_dir = os.path.join(settings.MEDIA_ROOT, analise.Name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    filtered_file = "{}_filtered.csv".format(analise.Name)
    pd.DataFrame.to_csv(df.df_filtered, os.path.join(output_dir, filtered_file))
    df_group = DfGroup(df.df_filtered)
    df_group.group_df(analise.WD, analise.WD_Start, analise.WD_Stop, analise.WD_Step)
    df_group.df_grouped = df_group.df_grouped.mean()

    group_file = "{}_group.csv".format(analise.Name)
    pd.DataFrame.to_csv(df_group.df_grouped, os.path.join(output_dir, group_file))

    graph = Graphs(df.df_filtered, df_group.df_grouped)
    graph.wind_rose(analise.WD, analise.WD_Step, os.path.join(output_dir, 'wd_rose.png'))
    graph.hist(analise.WS, os.path.join(output_dir, 'hist.png'))
    graph.time("AD_1", os.path.join(output_dir, 'time.png'))
    graph.ws_wd(analise.WD, analise.WS, os.path.join(output_dir, 'ws_wd.png'))

    return render(request, 'analize.html', {})