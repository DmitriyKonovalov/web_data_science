from django.contrib.auth.models import User
from django import forms


class UserFormEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
