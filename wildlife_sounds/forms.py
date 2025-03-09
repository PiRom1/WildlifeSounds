from django import forms
from django.forms import modelformset_factory
from .models import *



class LoginForm(forms.Form):
    
    username = forms.CharField(label = 'username', max_length = 100)
    password = forms.CharField(label = 'password', widget = forms.PasswordInput, max_length = 100)


class Listform(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name", "description"]
