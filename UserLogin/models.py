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
    email = models.EmailField(max_length=254, default=username)
    name = models.CharField(max_length=255)
    Birthday = models.CharField(max_length=10)
    # WalletMoney = models.IntegerField(default=)
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

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invitations_from")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invitations_to")
    accepted = models.BooleanField(default=False)

    # class Meta:
    #     verbose_name = _(u'friendship request')
    #     verbose_name_plural = _(u'friendship requests')
    #     unique_together = (('to_user', 'from_user'),)

    def __unicode__(self):
        return _(u'%(from_user)s wants to be friends with %(to_user)s') % \
                    {'from_user': unicode(self.from_user),'to_user': unicode(self.to_user)}

    def accept(self):
        Friendship.objects.befriend(self.from_user, self.to_user)
        self.accepted = True
        self.save()

    def cancel(self):
        self.delete()

class FriendshipManager(models.Manager):
    def friends_of(self, user, shuffle=False):
        qs = User.objects.filter(friendship__friends__user=user)
        if shuffle:
            qs = qs.order_by('?')
        return qs

    def are_friends(self, user1, user2):
        return bool(Friendship.objects.get(user=user1).friends.filter(user=user2).exists())

    def befriend(self, user1, user2):
        Friendship.objects.get(user=user1).friends.add( Friendship.objects.get(user=user2))
        # Now that user1 accepted user2's friend request we should delete any
        # request by user1 to user2 so that we don't have ambiguous data
        FriendshipRequest.objects.filter(from_user=user1,to_user=user2).delete()

    def unfriend(self, user1, user2):
        # Break friendship link between users
        Friendship.objects.get(user=user1).friends.remove(Friendship.objects.get(user=user2))
        # Delete FriendshipRequest's as well
        FriendshipRequest.objects.filter(from_user=user1,to_user=user2).delete()
        FriendshipRequest.objects.filter(from_user=user2,to_user=user1).delete()


class Friendship(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='friendship')
    friends = models.ManyToManyField('self', symmetrical=True)

    objects = FriendshipManager()

    # class Meta:
    #     verbose_name = _(u'friendship')
    #     verbose_name_plural = _(u'friendships')

    def __unicode__(self):
        return _(u'%(user)s\'s friends') % {'user': unicode(self.user)}

    def friend_count(self):
        return self.friends.count()
    friend_count.short_description = _(u'Friends count')

    def friend_summary(self, count=7):
        friend_list = self.friends.all().select_related(depth=1)[:count]
        return u'[%s%s]' % (u', '.join(unicode(f.user) for f in friend_list),
                            u', ...' if self.friend_count() > count else u'')
    friend_summary.short_description = _(u'Summary of friends')
