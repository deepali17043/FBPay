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

def get_pending_requests(user):
    all = FriendshipRequest.objects.all()
    for x in all:
        print(x.to_user," ************* ")
    frds1 = FriendshipRequest.objects.filter(to_user=user, accepted=False)
    return frds1


def ProfileView(request):
    user = User.object.get(username=request.user)
    reqs = get_pending_requests(user)
    print("-----------------heloo=------------")
    requests = list()
    for x in reqs:
        requests.append(x.from_user.username)
    return render(request, 'base.html', {'user': user, 'reqs': requests})


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


def send_requests_to(user1):
    all = User.object.all()
    frds1 = FriendshipRequest.objects.filter(from_user=user1)
    frds2 = FriendshipRequest.objects.filter(to_user=user1)
    for name in frds1:
        all = all.exclude(username=name.to_user)
    for name in frds2:
        all = all.exclude(username=name.from_user)
    all = all.exclude(username=user1)
    return all


def other_profile(request, username):
    user = User.object.get(username=username)
    frds = send_requests_to(request.user)
    return render(request,'profile.html',{'user':user, 'frds':frds})

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
    frds = send_requests_to(request.user)
    return render(request, 'find_friends.html', {'friends':frds})

def accept(request, username):
    user1 = User.object.get(username =request.user)
    user2 = User.object.get(username=username)
    exist = FriendshipRequest.objects.filter(from_user=user2, to_user=user1, accepted=False)
    if exist:
        list(exist)[0].accept()
    else:
        raise Http404("sorry, this user did not send you a friend request")
    return redirect('accounts/profile')
