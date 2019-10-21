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
from .models import Groups,Group_mem,Group_messages,GroupRequest

class OptionsView(TemplateView):
    template_name = 'options.html'


def get_pending_requests(user):
    all = FriendshipRequest.objects.all()
    frds1 = FriendshipRequest.objects.filter(to_user=user, accepted=False)
    return frds1


def url_correction(request):
    if request.user.is_authenticated:
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    else:
        url = request.build_absolute_uri('?')
    print(url)
    return redirect(url)


def grp_requests(user):
    all = Groups.objects.filter(group_admin=user)
    reqs = list()
    for elm in all:
        reqs.append(GroupRequest.objects.filter(group=elm))
    return reqs


def ProfileView(request):
    user = User.object.get(username=request.user)
    reqs = get_pending_requests(user)
    posts = Timeline.objects.filter(from_t=request.user, to_t=request.user)
    greqs = grp_requests(user)
    return render(request, 'newsfeed.html', {'user': user, 'freqs': reqs, 'posts': posts,'greqs':greqs})


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def logoutuser(request, username):
    user = User.object.get(username=username)
    user.unauthenticateuser()
    return redirect('logout')


def walletview(request):
    # print(username)
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    return render(request, 'ewallet.html', {'balance': user.balance})


def groups(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    grp = Group_mem.objects.filter(user=user)
    for el in grp:
        print(el.group.group_name)
    return render(request, 'groups.html', {'grp':grp})


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
#
# def is_friend(user1,user2):
#     x = Friendship.objects.filter(user1=user1)
#     y = Friendship.objects.filter(user2=user1)
#     friends = list()
#     for elm in x:
#         friends.append(elm.user2.username)
#     for elm in y:
#         friends.append(elm.user1.username)
#     is_frd = False
#     if(user2.username) in friends:
#         is_frd = True
#     return is_frd


def other_profile(request, username):
    user1 = User.object.get(username=request.user)
    user = User.object.get(username=username)
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
    time = user.timeline
    post = user.privacy
    data = Timeline.objects.filter(to_t=user)
    is_frd = Friendship.objects.filter(user1=user1,user2=user) | Friendship.objects.filter(user1=user,user2=user1)
    for elm in reqs:
        print(elm,"----*******----------")
    return render(request, 'profile.html', {'user': user, 'reqs':reqs, 'pub': time,'post':post, 'data': data, 'is_friend':is_frd})


def add_money(request):
    # print(username)
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        print(user.username)
        raise Http404("user not logged in")
    #val = request.POST.get("val","")
    user.balance = user.balance + 10
    user.save()
    return render(request, 'ewallet.html', {'user': user})



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
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/find"
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
    selfp = True
    if not user1 == user2:
        selfp = False
    Timeline.objects.create(from_t=user1, to_t=user2, post=request.POST.get("timeline_post", ""),selfp=selfp)
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    return redirect(url)

def settings(request):
    user = User.object.get(username=request.user)
    if not request.user.is_authenticated:
        raise Http404("user not logged in")
    return render(request, 'settings.html',{'user':request.user})


def deduct(user,val):
    user.balance = user.balance - val

def set_settings(request):
    user = User.object.get(username=request.user)
    priv = request.POST.get("priv","")
    u_type = request.POST.get("u_type","")
    pr_S = request.POST.get("pr_s","")
    if priv =="yes":
        user.privacy = True
    else:
        user.privacy = False
    if u_type == "casual":
        user.type = 1
    elif u_type == "premium":
        if pr_S == "s":
            user.type = 2
            deduct(user,50)  #to be done monthly
        elif pr_S =='g':
            user.type = 3
            deduct(user,100) #to be done monthly
        elif pr_S =='p':
            user.type = 4
            deduct(user,150) #to be done monthly
        else:
            user.type = 2
            deduct(user,50)  #to be done monthly
    elif u_type == "comm":
        user.type = 5
        deduct(user,5000) #to be done yearly
    else:
        user.type =1

    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    user.save()
    return redirect(url)

def grp_to_join(user1):
    #Groups.objects.create(group_name="No lifers",group_admin=user1)
    all = Groups.objects.all()
    grps1 = GroupRequest.objects.filter(fro=user1,acc=False)
    grps2 = Group_mem.objects.filter(user=user1)
    grps = list()
    for elm in grps1:
        grps.append(elm.group.group_name)
    for elm in grps2:
        grps.append(elm.group.group_name)
    send = list()
    for elm in all:
        if elm.group_name not in grps:
            send.append(elm)
    return send


def join_grp(request):
    grps = grp_to_join(request.user)
    return render(request, 'join_groups.html', {'grps': grps})


def user_to_grp(request,groupname):
    grp = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=request.user)
    if not grp.group_closed:
        Group_mem.objects.create(user=user,group=grp)
    else:
        GroupRequest.objects.create(group=grp, fro=user)
        print("group_request_sent")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    print(url)
    return redirect(url)

def group_box(request,groupname):
    print("innn here-----")
    user = User.object.get(username=request.user)
    group = Groups.objects.get(group_name=groupname)
    mess = Group_messages.objects.filter(group=group)
    mess = mess.order_by('datetime')
    for element in mess:
        print(element.user.username, ":")
        print(element.message)
    return render(request, 'groupbox.html', {'mess': mess, 'groupname': group.group_name})


def create_grp(request):
    user = User.object.get(username=request.user)
    c = request.POST.get("closed", "")
    grp = False
    if c == "yes":
        grp = True
    Groups.objects.create(group_name=request.POST.get("grp_name", ""),group_admin=user, group_closed=grp)
    Group_mem.objects.create(user=user,group=Groups.objects.get(group_name=request.POST.get("grp_name", "")))
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/groups"
    return redirect(url)


def grp_send(request,groupname):
    user = User.object.get(username=request.user)
    grp = Groups.objects.get(group_name=groupname)
    Group_messages.objects.create(user=user, group=grp, message=request.POST.get("message", ""))
    return group_box(request, groupname)


def grp_accept(request,groupname,username):
    group = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=username)
    print(username,"kjdsku I sent this")
    exist = GroupRequest.objects.filter(group=group,fro=user, acc=False)
    if exist:
        Group_mem.objects.create(user=user,group=group)
        GroupRequest.objects.filter(group=group,fro=user).delete()
    else:
        raise Http404("sorry, this user did not send you a group request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    print(url)
    return redirect(url)

def grp_decline(request,groupname,username):
    group = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=username)
    exist = GroupRequest.objects.filter(group=group,fro=user, acc=False)
    if exist:
        #Group_mem.objects.create(user=user,group=group)
        GroupRequest.objects.filter(group=group,fro=user).delete()
    else:
        raise Http404("sorry, this user did not send you a group request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    print(url)
    return redirect(url)