from django import forms
from .models import UserModel
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())


class UserCreateForm(UserCreationForm):
    profile_pic = forms.FileField()

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_pic']




