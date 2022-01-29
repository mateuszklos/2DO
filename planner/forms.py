from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput

from .models import Task
from django import forms


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='username')
    password1 = forms.CharField(widget=forms.PasswordInput, label='password', max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput, label='confirm password', max_length=50)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False

    class Meta:
        model = Task
        fields = ['title']
        exclude = ['user']
        widgets = {
            'title': TextInput(attrs={'autofocus': 'autofocus'})
        }

