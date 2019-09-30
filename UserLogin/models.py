from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from abc import ABC, abstractmethod


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Username must be set!')
        user = self.model(username=username, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None):
        user = self.create_user(username, name, password)
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
    is_active = models.BooleanField(default=True)
    # this field is required to login super user from admin panel
    is_staff = models.BooleanField(default=True)
    # this field is required to login super user from admin panel
    is_superuser = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'username'
