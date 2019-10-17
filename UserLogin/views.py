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

def other_profile(request, username):
    user = User.object.get(username=username)
    all = User.object.all()
    return render(request,'profile.html',{'user':user, 'frds':all})

def add_money(request, username):
    #print(username)
    user = User.object.get(username=username)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request,'ewallet.html',{'balance':user.balance})

def friends(request):
    x = FriendshipRequest.objects.filter(from_user=request.user)
    return render(request, 'friends.html', {'friends': x})


def addfriend(request, username):
    #print(username)
    user2 = User.object.get(username=username)
    user1 = request.user
    FriendshipRequest.objects.create(from_user=request.user,to_user=user2)
    print("request_sent")
    url = request.build_absolute_uri('/').strip("/")+"/"+user2.username+"/timeline"
    print(url)
    return redirect(url)

def find_friends(request):
    #
    all1 = User.object.all()
    # all = FriendshipRequest.objects.all()
    # for x in all:
    #      x.delete()
    # # --------------------------------------
    #print(frds)
    # all = User.object.all()
    # for name in all:
    #     for nm in all:
    #         FriendshipRequest.objects.create(from_user=name, to_user=nm)
    # print(request.user," -----------------")
    frds1 = FriendshipRequest.objects.filter(from_user=request.user)
    frds2 = FriendshipRequest.objects.filter(to_user=request.user)
    for name in frds1:
        all1 = all1.exclude(username=name.to_user)
    for name in frds2:
        all1 = all1.exclude(username=name.from_user)
    all1 = all1.exclude(username=request.user)
    # print("-----------------------")
    # for x in all1:
    #     print(x)
    return render(request, 'find_friends.html', {'friends':all1})