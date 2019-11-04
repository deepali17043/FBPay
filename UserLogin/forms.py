from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from captcha.fields import CaptchaField



class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "name", "Birthday", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
