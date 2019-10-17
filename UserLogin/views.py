from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpRequest

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, FriendshipRequest

class OptionsView(TemplateView):
    template_name = 'options.html'


class ProfileView(TemplateView):
    template_name = 'base.html'


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def logoutuser(request, username):
    user = User.object.get(username=username)
    user.unauthenticateuser()
    return redirect('logout')


def walletview(request, username):
    #print(username)
    user = User.object.get(username=username)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request,'ewallet.html',{'balance':user.balance})

def add_money(request, username):
    #print(username)
    user = User.object.get(username=username)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request,'ewallet.html',{'balance':user.balance})

def Fflist(request):
    x = FriendshipRequest.objects.filter(from_user=request.user)
    return HttpResponse("<h1>Friends</h1>{0}".format(x))