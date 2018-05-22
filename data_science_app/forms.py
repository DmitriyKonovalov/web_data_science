from django import forms
from django.contrib.auth.models import User

from data_science_app.models import Analise


class User_Form(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class User_Form_Edit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class New_Analise_Form(forms.ModelForm):
    #    user = forms.ModelChoiceField(queryset=Analise.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Analise
        fields = ('user', 'Name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'Date_Create',
                  'Date_Modified', 'File_Data')


class Edit_Analise_Form(forms.ModelForm):
    class Meta:
        model = Analise
        fields = (
        'Name', 'WS', 'WD', 'WD_Step', 'WD_Start', 'WD_Stop', 'WS_Start', 'WS_Stop', 'Date_Modified', 'File_Data')
