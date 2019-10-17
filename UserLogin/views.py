from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.http import HttpResponse
import UserLogin.models as m


class OptionsView(TemplateView):
    template_name = 'options.html'


class ProfileView(TemplateView):
    template_name = 'base.html'


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# def student_show(request):
#     x = []
#     for i in range(10):
#         x.append(i)
#     return HttpResponse("<h1>Friends</h1>{0}".format(x))


def Fflist(request):
    x = m.FriendshipRequest.objects.filter(from_user=request.user)
    return HttpResponse("<h1>Friends</h1>{0}".format(x))
