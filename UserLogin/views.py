from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, FriendshipRequest, Friendship, MessageBox, Timeline
from .models import Groups, Group_mem, Group_messages, GroupRequest, AccountSummary, Pages, PageContent
from .transactions import OTPVerifier
import time
from datetime import date
from random import shuffle


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
    # print(url)
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
    posts = Timeline.objects.filter(from_t=request.user) | Timeline.objects.filter(to_t=request.user)
    greqs = grp_requests(user)
    grpadm = False
    if request.user == 'kriti' or request.user == 'dee' or request.user == 'shree':
        grpadm = True
    return render(request, 'newsfeed.html',
                  {'user': user, 'freqs': reqs, 'posts': posts, 'greqs': greqs, 'grpadm': grpadm})


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def __init__(self):
        frm = CustomUserCreationForm()
        if frm.is_valid():
            raise Http404("Cannot validate that you're a human")
        if User.object.all().count() < 50:
            self.template_name = 'signup.html'
            redirect('accounts/profile/')
        else:
            raise Http404('Cannot accept more users. Limit exceeded.')


def logoutuser(request, username):
    user = User.object.get(username=username)
    user.unauthenticateuser()
    return redirect('logout')


def walletview(request):
    # print(username)
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        # print(user.username)
        raise Http404("user not logged in")
    return render(request, 'ewallet.html', {'balance': user.balance})


def groups(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    grp = Group_mem.objects.filter(user=user)
    # for el in grp:
    # print(el.group.group_name)
    flag = True
    if user.type == 1:
        flag = False
    return render(request, 'groups.html', {'grp': grp, 'bol': flag})


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
    post = False
    if user.username in friends:
        post = user.privacy
    data = Timeline.objects.filter(to_t=user)
    is_frd = Friendship.objects.filter(user1=user1, user2=user) | Friendship.objects.filter(user1=user, user2=user1)
    # for elm in reqs:
    # print(elm,"----*******----------")
    return render(request, 'profile.html',
                  {'user': user, 'reqs': reqs, 'pub': time, 'post': post, 'data': data, 'is_friend': is_frd})


def addmoneyView(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    return render(request, 'addmoney.html', {'user': user})


def friends(request):
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    friends = list()
    for elm in x:
        friends.append(elm.user2)
    for elm in y:
        friends.append(elm.user1)
    return render(request, 'friends.html', {'friends': friends})


def addfriend(request, username):
    # print(username)
    user2 = User.object.get(username=username)
    user1 = request.user
    FriendshipRequest.objects.create(from_user=request.user, to_user=user2)
    # print("request_sent")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/find"
    # print(url)
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
            reqs.append(elm)
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
        # print(user2.username, "JA RAHA HAIIII")
        all = FriendshipRequest.objects.all()
        for x in all:
            if (x.from_user == user2 and x.to_user == user1):
                x.delete()
    else:
        raise Http404("sorry, this user did not send you a friend request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    # print(url)
    return redirect(url)


def add_message(request, username):
    # print('shree')
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    message = request.POST.get("message", "")
    if not message == "":
        # print(request.method)
        MessageBox.objects.create(from_m=user1, to_m=user2, message=request.POST.get("message", ""))
        # print(request.POST.get("message", ""), ".................")
    return messagebox(request, username)


def messenger(request):
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    all = User.object.exclude(username=request.user)

    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    fl = False
    if request.user.type == 5:
        fl = True

    user = User.object.get(username=request.user)
    lis = MessageBox.objects.filter(to_m=user)
    li = list()
    for i in lis:
        if i.from_m.username not in friends:
            if i.from_m.username not in li:
                li.append(i.from_m.username)

    return render(request, 'message.html', {'friends': friends, 'bol': fl, 'all': all, 'li': li})


def messagebox(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    mess = MessageBox.objects.filter(from_m=user1, to_m=user2) | MessageBox.objects.filter(from_m=user2, to_m=user1)
    mess = mess.order_by('datetime')
    # for element in mess:
    #     print(element.from_m, ":")
    #     print(element.message)
    return render(request, 'messagebox.html', {'mess': mess, 'username': username})


def add_post(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    selfp = True
    if not user1 == user2:
        selfp = False
    Timeline.objects.create(from_t=user1, to_t=user2, post=request.POST.get("timeline_post", ""), selfp=selfp)
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    return redirect(url)


def settings(request):
    user = User.object.get(username=request.user)
    if not request.user.is_authenticated:
        raise Http404("user not logged in")
    return render(request, 'settings.html', {'user': request.user})


def deduct(user, val):
    if user.balance - val < 0:
        raise Http404('Insufficient Balance')
    user.balance = user.balance - val
    AccountSummary.objects.create(from_t=user, to_t=user, amtsent=-val, balance1=user.balance, balance2=user.balance,
                                  selfp=True)


def setpriv(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    priv = request.POST.get("priv", "")
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    GenerationTime = time.time()
    GeneratedToken = OTPVerifierObject.GenerateToken()
    return render(request, 'settings.html',
                  {'user': user, 'time': GenerationTime, 'sent2': True, 'pri': priv, 'x': virkey()})


def setprivverify(request, Time, pri):
    user = User.object.get(username=request.user)
    UserToken = int(request.POST.get("otp", ""))
    # Time = time
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    t = False
    while time.time() <= float(Time) + OTPVerifierObject.TokenValidityTime:
        t = OTPVerifierObject.VerifyToken(UserToken, tolerance=1)
    if t:
        if pri == "yes":
            user.privacy = True
        else:
            user.privacy = False
        user.save()
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/"
        return redirect(url)
    else:
        raise Http404('Incorrect OTP entered')


def setutype(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    u_type = request.POST.get("u_type", "")
    pr_S = request.POST.get("pr_s", "")
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    GenerationTime = time.time()
    GeneratedToken = OTPVerifierObject.GenerateToken()
    return render(request, 'settings.html',
                  {'user': user, 'time': GenerationTime, 'sent1': True, 'chngto': u_type, 'prsub': pr_S})


def setutypeverify(request, Time, chngto):
    user = User.object.get(username=request.user)
    UserToken = int(request.POST.get("otp", ""))
    # Time = time
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    t = False
    while time.time() <= float(Time) + OTPVerifierObject.TokenValidityTime:
        t = OTPVerifierObject.VerifyToken(UserToken, tolerance=1)
    if t:
        if chngto == "casual":
            user.type = 1
        elif chngto == "s":
            user.type = 2
            deduct(user, 50)  # to be done monthly
        elif chngto == 'g':
            user.type = 3
            deduct(user, 100)  # to be done monthly
        elif chngto == 'p':
            user.type = 4
            deduct(user, 150)  # to be done monthly
        elif chngto == "comm":
            user.type = 5
            deduct(user, 5000)  # to be done yearly
        else:
            user.type = 1
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
        user.save()
        return redirect(url)
    else:
        raise Http404('Incorrect OTP entered')


def grp_to_join(user1):
    # Groups.objects.create(group_name="No lifers",group_admin=user1)
    all = Groups.objects.all()
    grps1 = GroupRequest.objects.filter(fro=user1, acc=False)
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
    return render(request, 'join_groups.html', {'grps': grps, 'sent': False})


def user_to_grp(request, groupname):
    grp = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        # print(user.username)
        raise Http404("user not logged in")
    grps = grp_to_join(request.user)
    if not grp.group_closed:
        Group_mem.objects.create(user=user, group=grp)
    else:
        if not grp.group_price == 0:
            OTPVerifierObject = OTPVerifier()
            OTPVerifierObject.setuser(request.user)
            GenerationTime = time.time()
            GeneratedToken = OTPVerifierObject.GenerateToken()
            return render(request, 'join_groups.html',
                          {'user': user, 'grps': grps, 'time': GenerationTime, 'sent': True, 'gp': grp})
        else:
            GroupRequest.objects.create(group=grp, fro=user)
        # print("group_request_sent")
    url = request.build_absolute_uri('/').strip("/") + "/grp_find"
    # print(url)
    return redirect(url)


def group_box(request, groupname):
    # print("innn here-----")
    user = User.object.get(username=request.user)
    group = Groups.objects.get(group_name=groupname)
    flag = False
    if user == group.group_admin:
        flag = True
    mess = Group_messages.objects.filter(group=group)
    mess = mess.order_by('datetime')
    # for element in mess:
    #     print(element.user.username, ":")
    #     print(element.message)
    return render(request, 'groupbox.html', {'mess': mess, 'groupname': group.group_name, 'flag': flag})


def create_grp(request):
    user = User.object.get(username=request.user)
    if request.POST.get("grp_name", "") == '':
        raise Http404('Group name cannot be empty. Try again, by entering a valid group name :)')
    c = request.POST.get("closed", "")
    grp = False
    if c == "yes":
        grp = True
    # print(Groups.objects.filter(group_admin=user, group_closed=True).count(),"hhhh")
    # print(user.type,"usertype")
    if user.type == 2 and Groups.objects.filter(group_admin=user, group_closed=True).count() > 1:
        raise Http404("sorry cannot create more groups")
    elif user.type == 3 and Groups.objects.filter(group_admin=user, group_closed=True).count() > 3:
        raise Http404("sorry cannot create more groups")

    p = request.POST.get("price", "")
    if user.type == 1:
        p = 0
    Groups.objects.create(group_name=request.POST.get("grp_name", ""), group_admin=user, group_closed=grp,
                          group_price=p)
    Group_mem.objects.create(user=user, group=Groups.objects.get(group_name=request.POST.get("grp_name", "")))
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/groups"
    return redirect(url)


def grp_send(request, groupname):
    user = User.object.get(username=request.user)
    grp = Groups.objects.get(group_name=groupname)
    message = request.POST.get("message", "")
    if not message == "":
        Group_messages.objects.create(user=user, group=grp, message=message)
    return group_box(request, groupname)


def grp_accept(request, groupname, username):
    group = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=username)
    exist = GroupRequest.objects.filter(group=group, fro=user, acc=False)
    if exist:
        Group_mem.objects.create(user=user, group=group)
        user.balance = user.balance - group.group_price
        user.save()
        AccountSummary.objects.create(from_t=user, to_t=user, amtsent=-group.group_price, balance1=user.balance,
                                      balance2=user.balance, selfp=True)
        GroupRequest.objects.filter(group=group, fro=user).delete()
    else:
        raise Http404("sorry, this user did not send you a group request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    # print(url)
    return redirect(url)


def grp_decline(request, groupname, username):
    group = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=username)
    exist = GroupRequest.objects.filter(group=group, fro=user, acc=False)
    if exist:
        # Group_mem.objects.create(user=user,group=group)
        GroupRequest.objects.filter(group=group, fro=user).delete()
    else:
        raise Http404("sorry, this user did not send you a group request")
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile"
    # print(url)
    return redirect(url)


def Transactionsend(request):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        # print(user.username)
        raise Http404("user not logged in")

    tod = date.today()
    # print(tod)
    summary = AccountSummary.objects.filter(from_t=user, datetime__month=tod.month) | AccountSummary.objects.filter(
        to_t=user, datetime__month=tod.month)
    no_trans = summary.count()
    # print(no_trans, "************")
    if user.type == 1 and no_trans > 15:
        raise Http404("Exceeded limit of transaction")
    elif (user.type == 2 or user.type == 3 or user.type == 4) and no_trans > 30:
        raise Http404("Exceeded limit of transaction")

    amt = request.POST.get("amt", "")
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    GenerationTime = time.time()
    GeneratedToken = OTPVerifierObject.GenerateToken()
    return render(request, 'addmoney.html',
                  {'user': user, 'time': GenerationTime, 'sent': True, 'amt': amt, 'x': virkey()})


def Transactionverify(request, Time, amt):
    user = User.object.get(username=request.user)
    UserToken = int(request.POST.get("otp", ""))
    # Time = time
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    t = False
    while time.time() <= float(Time) + OTPVerifierObject.TokenValidityTime:
        t = OTPVerifierObject.VerifyToken(UserToken, tolerance=1)
    if t:
        user.balance = user.balance + int(amt)
        user.save()
        AccountSummary.objects.create(from_t=user, to_t=user, amtsent=int(amt), balance1=user.balance,
                                      balance2=user.balance, selfp=True)
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/ewallet"
        return redirect(url)
    else:
        raise Http404('Incorrect OTP entered')


def send_money(request):
    x = Friendship.objects.filter(user1=request.user)
    y = Friendship.objects.filter(user2=request.user)
    friends = list()
    for elm in x:
        friends.append(elm.user2.username)
    for elm in y:
        friends.append(elm.user1.username)
    return render(request, 'send_money.html', {'friends': friends})


def send_money_to(request, username):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        raise Http404("user not logged in")
    return render(request, 'sendmoneyform.html', {'user': user, 'username': username})


def Transactionsendto(request, username):
    user = User.object.get(username=request.user)
    if user.isauthenticated() == 1:
        # print(user.username)
        raise Http404("user not logged in")
    amt = request.POST.get("amt", "")
    if (user.balance - int(amt) < 0):
        raise Http404("Insufficient balance")
    tod = date.today()
    # print(tod)
    summary = AccountSummary.objects.filter(from_t=user, datetime__month=tod.month) | AccountSummary.objects.filter(
        to_t=user, datetime__month=tod.month)
    no_trans = summary.count()
    # print(no_trans,"************")
    if user.type == 1 and no_trans > 15:
        raise Http404("Exceeded limit of transaction")
    elif (user.type == 2 or user.type == 3 or user.type == 4) and no_trans > 30:
        raise Http404("Exceeded limit of transaction")

    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    GenerationTime = time.time()
    GeneratedToken = OTPVerifierObject.GenerateToken()
    return render(request, 'sendmoneyform.html',
                  {'user': user, 'time': GenerationTime, 'sent': True, 'amt': amt, 'username': username, 'x': virkey()})


def transverify(request, username, Time, amt):
    user2 = User.object.get(username=username)
    user1 = User.object.get(username=request.user)
    UserToken = int(request.POST.get("otp", ""))
    # Time = time
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    t = False
    while time.time() <= float(Time) + OTPVerifierObject.TokenValidityTime:
        t = OTPVerifierObject.VerifyToken(UserToken, tolerance=1)
    if t:
        user1.balance = user1.balance - int(amt)
        user1.save()
        user2.balance = user2.balance + int(amt)
        user2.save()
        AccountSummary.objects.create(from_t=user1, to_t=user2, amtsent=int(amt), balance1=user1.balance,
                                      balance2=user2.balance, selfp=False)
        url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/ewallet"
        return redirect(url)
    else:
        raise Http404('Incorrect OTP entered')


def summary_acc(request):
    user1 = User.object.get(username=request.user)
    summary = AccountSummary.objects.filter(from_t=user1) | AccountSummary.objects.filter(to_t=user1)
    summary = summary.order_by('-datetime')
    return render(request, 'account.html', {'summary': summary, 'user': user1})


def pages(request):
    li = Pages.objects.all()
    user = User.object.get(username=request.user)
    flag = False
    if user.type == 5:
        flag = True
    return render(request, 'pages.html', {'pg': li, 'user': user, 'bol': flag})


def create_page(request):
    user = User.object.get(username=request.user)
    Pages.objects.create(name=request.POST.get("pgnm", ""), admin=user)
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/pages"
    return redirect(url)


def viewpg(request, pgname):
    user = User.object.get(username=request.user)
    pg = Pages.objects.get(name=pgname)
    opt = False
    if user == pg.admin:
        opt = True
    psts = PageContent.objects.filter(page=pg)
    psts = psts.order_by('-datetime')
    return render(request, 'pgbox.html', {'posts': psts, 'pg': pg, 'opt': opt})


def post_pg(request, pgname):
    user = User.object.get(username=request.user)
    pg = Pages.objects.get(name=pgname)
    post = request.POST.get("pst", "")
    if not post == "":
        PageContent.objects.create(page=pg, post=post)
    return viewpg(request, pgname)


def sendtogrp(request, Time, groupname):
    grp = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=request.user)
    UserToken = int(request.POST.get("otp", ""))
    OTPVerifierObject = OTPVerifier()
    OTPVerifierObject.setuser(request.user)
    t = False
    while time.time() <= float(Time) + OTPVerifierObject.TokenValidityTime:
        t = OTPVerifierObject.VerifyToken(UserToken, tolerance=1)
    if t:
        GroupRequest.objects.create(group=grp, fro=user)
        url = request.build_absolute_uri('/').strip("/") + "/grp_find"
        return redirect(url)
    else:
        raise Http404('Incorrect OTP entered')


def virkey():
    x = [[i] for i in range(10)]
    shuffle(x)
    return x


def remuser(request, groupname):
    grp = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=request.user)
    mem = Group_mem.objects.filter(group=grp)
    li = list()
    for e in mem:
        if not e.user == user:
            li.append(e.user)
    return render(request, 'removeuser.html', {'li': li, 'user': user, 'grp': grp})


def remove_user(request, username, groupname):
    # print("ttttttttttttttttt")
    grp = Groups.objects.get(group_name=groupname)
    user = User.object.get(username=username)
    if not request.user == grp.group_admin:
        raise Http404('You do not have the authority to remove users')
    Group_mem.objects.filter(group=grp, user=user).delete()
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/groups"
    return redirect(url)


def HomePage(request):
    url = request.build_absolute_uri('/').strip("/") + "/login"
    return redirect(url)


def unfriend(request, username):
    user = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    x = Friendship.objects.filter(user1=user, user2=user2)
    if x:
        x.delete()
    y = Friendship.objects.filter(user1=user2, user2=user)
    if y:
        y.delete()
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/FriendList.html"
    return redirect(url)


def user_del(request):
    user = User.object.get(username=request.user)
    all = User.object.exclude(username=request.user)
    return render(request, 'userdel.html', {'user': user, 'all': all})


def fakeuserdel(request, username):
    user1 = User.object.get(username=request.user)
    user2 = User.object.get(username=username)
    if not (request.user == 'kriti' or request.user == 'dee' or request.user == 'shree'):
        raise Http404('You do not have the authority to remove users')
    User.object.filter(username=user2.username).delete()
    url = request.build_absolute_uri('/').strip("/") + "/accounts/profile/userdel"
    return redirect(url)


