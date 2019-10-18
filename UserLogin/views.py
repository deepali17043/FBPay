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
from .models import User, FriendshipRequest, Friendship, MessageBox, Timeline


class OptionsView(TemplateView):
    template_name = 'options.html'


def get_pending_requests(user):
    all = FriendshipRequest.objects.all()
    for x in all:
        print(x.to_user, " ************* ")
    frds1 = FriendshipRequest.objects.filter(to_user=user, accepted=False)
    return frds1


def url_correction(request):
    if request.user.is_authenticated:
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    else:
        url = request.build_absolute_uri('?')
    print(url)
    return redirect(url)


def ProfileView(request):
    user = User.object.get(username=request.user)
    reqs = get_pending_requests(user)
    requests = list()
    for x in reqs:
        requests.append(x.from_user.username)
    posts = Timeline.objects.filter(from_t=request.user, to_t=request.user)
    return render(request, 'newsfeed.html', {'user': user, 'reqs': requests, 'posts': posts})


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def logoutuser(request, username):
    user = User.object.get(username=username)
    user.unauthenticateuser()
    return redirect('logout')


def walletview(request, username):
    # print(username)
    user = User.object.get(username=username)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request, 'ewallet.html', {'balance': user.balance})


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

def is_friend(user1,user2):
    x = Friendship.objects.filter(user1=user1)
    y = Friendship.objects.filter(user2=user1)
    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    is_frd = False
    if(user2.username) in friends:
        is_frd = True
    return is_frd


def other_profile(request, username):
    user1 = User.object.get(username=request.user)
    user = User.object.get(username=username)
    frds = send_requests_to(request.user)

    yes = user.privacy
    data = Timeline.objects.filter(to_t=user)
    is_frd = is_friend(user1,user)
    return render(request, 'profile.html', {'user': user, 'frds': frds, 'pub': yes, 'data': data, 'is_friend':is_frd})


def add_money(request, username):
    # print(username)
    user = User.object.get(username=username)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request, 'ewallet.html', {'balance': user.balance})



def friends(request):
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    return render(request, 'friends.html', {'friends': friends})


def addfriend(request, username):
    # print(username)
    user2 = User.object.get(username=username)
    user1 = request.user
    FriendshipRequest.objects.create(from_user=request.user, to_user=user2)
    print("request_sent")
    url = request.build_absolute_uri('/').strip("/") + "/" + user2.username + "/timeline"
    print(url)
    return redirect(url)


def find_friends(request):
    frds = send_requests_to(request.user)
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    reqs = list()
    for elm in frds:
        if elm.username not in friends:
            reqs.append(elm.username)
    # all = Friendship.objects.all()
    # for x in all:
    #      x.delete()
    return render(request, 'find_friends.html', {'friends': reqs})


def accept(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    exist = FriendshipRequest.objects.filter(from_user=user2, to_user=user1, accepted=False)
    if exist:
        Friendship.objects.create(user1=user1, user2=user2)
        FriendshipRequest.objects.filter(from_user=user2, to_user=user1).delete()
    else:
        raise Http404("sorry, this user did not send you a friend request")
    # url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    # print(url)
    # return redirect(url)
    return url_correction(request)


def decline(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    exist = FriendshipRequest.objects.filter(from_user=user2, to_user=user1, accepted=False)
    if exist:
        print(user2.username, "JA RAHA HAIIII")
        all = FriendshipRequest.objects.all()
        for x in all:
            if (x.from_user == user2 and x.to_user == user1):
                x.delete()
    else:
        raise Http404("sorry, this user did not send you a friend request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    print(url)
    return redirect(url)


def add_message(request, username):
    # print('shree')
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    # print(request.method)
    MessageBox.objects.create(from_m=user1, to_m=user2, message=request.POST.get("message", ""))
    # print(request.POST.get("message", ""), ".................")
    return messagebox(request, username)


def messenger(request):
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    return render(request, 'message.html', {'friends': friends})


def messagebox(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    mess = MessageBox.objects.filter(from_m=user1, to_m=user2) | MessageBox.objects.filter(from_m=user2, to_m=user1)
    mess = mess.order_by('datetime')
    for element in mess:
        print(element.from_m, ":")
        print(element.message)
    return render(request, 'messagebox.html', {'mess': mess, 'username': username})


def add_post(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    Timeline.objects.create(from_t=user1, to_t=user2, post=request.POST.get("timeline_post", ""))
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    return redirect(url)

def settings(request):
    user = User.object.get(username=request.user)
    if not request.user.is_authenticated:
        raise Http404("user not logged in")
    return render(request, 'settings.html',{'user':request.user})
