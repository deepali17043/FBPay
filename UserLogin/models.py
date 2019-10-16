from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from abc import ABC, abstractmethod


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Username must be set!')
        user = self.model(username=username, name=name,authenticated=1)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, username, password, authenticated=1)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


# When including different types of users, convert this class into an abstract class
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    # password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    Birthday = models.CharField(max_length=10)
    # WalletMoney = models.IntegerField()
    balance = models.IntegerField(default=True)
    authenticated = models.IntegerField(default=True)
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
        #user = User.object.get(username=self.username).update(authenticated=True)
        user = User.object.get(username=self.username)
        user.Birthday = "199999999"
        user.authenticated = 0
        user.save()
        user1 = User.object.get(username=self.username)
        print(user1.Birthday,"hellllllll",user1.authenticated)
        return ''

    def unauthenticateuser(self):
        print('unauth called')
        self.authenticated = 1

    def isauthenticated(self):
        print(self.username)
        print(self.authenticated)
        return self.authenticated