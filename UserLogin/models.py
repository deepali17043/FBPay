from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from abc import ABC, abstractmethod

import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytz import unicode


class UserManager(BaseUserManager):
    def create_user(self, username, name, email, password=None):
        if not username:
            raise ValueError('Username must be set!')
        user = self.model(username=username, name=name, authenticated=1, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        print("email: ")
        email = input()
        user = self.create_user(username, username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


# When including different types of users, convert this class into an abstract class
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    # password = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=255)
    Birthday = models.CharField(max_length=10)
    # WalletMoney = models.IntegerField(default=)
    balance = models.IntegerField(default=1000)
    authenticated = models.IntegerField(default=1)
    privacy = models.BooleanField(default=True)
    timeline = models.BooleanField(default=True)
    type = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    # this field is required to login super user from admin panel
    is_staff = models.BooleanField(default=True)
    # this field is required to login super user from admin panel
    is_superuser = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'username'

    def authenticateuser(self):
        print(">>>>")
        print(self.authenticated)
        print(self.username)
        # user = User.object.get(username=self.username).update(authenticated=True)
        user = User.object.get(username=self.username)
        user.authenticated = 0
        user.save()
        user1 = User.object.get(username=self.username)
        return ''

    def unauthenticateuser(self):
        print('unauth called')
        self.authenticated = 1

    def isauthenticated(self):
        print(self.username)
        print(self.authenticated)
        return self.authenticated


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inv_from")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inv_to")
    accepted = models.BooleanField(default=False)

    # def unfriend(self, user1, user2):
    #
    #     Friendship.objects.get(user=user1).friends.remove(Friendship.objects.get(user=user2))
    #
    #     FriendshipRequest.objects.filter(from_user=user1,to_user=user2).delete()
    #     FriendshipRequest.objects.filter(from_user=user2,to_user=user1).delete()


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship2")


#   objects = FriendshipManager()


class MessageBox(models.Model):
    from_m = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_m1")
    to_m = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_m2")
    message = models.CharField(max_length=2500)
    datetime = models.DateTimeField(auto_now=True)


class Timeline(models.Model):
    from_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_t1")
    to_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_t2")
    post = models.CharField(max_length=2500)
    datetime = models.DateTimeField(auto_now=True)
    privacy = models.BooleanField(default=False)
    selfp = models.BooleanField(default=True)


class Groups(models.Model):
    group_name = models.CharField(max_length=200)
    group_closed = models.BooleanField(default=False)
    group_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grp_admin1")
    group_price = models.IntegerField(default=0)


class Group_mem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grp_mem")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="grp_name")


class Group_messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grp_mem1")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="grp_name1")
    message = models.CharField(max_length=2500)
    datetime = models.DateTimeField(auto_now=True)


class GroupRequest(models.Model):
    fro = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_r")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="to_r")
    acc = models.BooleanField(default=False)


class AccountSummary(models.Model):
    from_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from1")
    to_t = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to2")
    datetime = models.DateTimeField(auto_now=True)
    # mn = models.CharField(max_length=50,default="")
    amtsent = models.IntegerField()
    balance1 = models.IntegerField()
    balance2 = models.IntegerField()
    selfp = models.BooleanField(default=True)


class Pages(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=1000, unique=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adm")
    date = models.DateField(auto_now=True)


class PageContent(models.Model):
    page = models.ForeignKey(Pages, on_delete=models.CASCADE,related_name="pg")
    post = models.CharField(max_length=3000)
    datetime = models.DateTimeField(auto_now=True)

