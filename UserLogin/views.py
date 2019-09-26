from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


class LoginPage(TemplateView):
    template_name = 'login.html'


class ProfileView(TemplateView):
    template_name = 'base.html'

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
