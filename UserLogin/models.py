from django.db import models
# from abc import ABC, abstractmethod


# When including different types of users, convert this class into an abstract class
class User (models.Model):
    username = models.TextField()
    password = models.TextField()
    name = models.TextField()
    Birthday = models.CharField(max_length=10)
    WalletMoney = models.IntegerField()

