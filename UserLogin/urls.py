from . import views
from django.urls import path
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    #   path('', views.LoginPage.as_view(), name ='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/profile/', views.ProfileView, name='profile'),
    path('accounts/profile/options.html', views.OptionsView.as_view(), name='options'),
    path('accounts/profile/newsfeed.html', views.OptionsView.as_view(), name='newsfeed'),
    path('accounts/profile/notify.html', views.OptionsView.as_view(), name='notifications'),
    path('accounts/profile/ewallet/', views.walletview, name='ewallet'),
    url(r'^(?P<username>.+)/accept', views.accept, name='accept'),
    url(r'^(?P<username>.+)/decline', views.decline, name='decline'),
    url(r'^(?P<username>.+)/messages', views.messagebox, name='messagebox'),
    url(r'^(?P<username>.+)/timeline', views.other_profile, name='other_user'),
    url(r'^(?P<username>.+)/send_req', views.addfriend, name='request'),
    url(r'^(?P<username>.+)/logoutuser/', views.logoutuser, name='logoutuser'),
    url(r'^(?P<username>.+)/text/', views.add_message, name='text'),
    path('accounts/profile/FriendList.html', views.friends, name='F_list'),
    url(r'^(?P<username>.+)/post', views.add_post, name='post'),
    url(r'^(?P<username>.+)/frd_post', views.add_post, name='frd_post'),

    path('accounts/profile/find', views.find_friends, name='find_frd'),
    path('accounts/profile/messenger.html', views.messenger, name='messenger'),
    #   path('signup/',views.signup, name='new user')

    path('accounts/profile/settings', views.settings, name='settings'),
    path('set_settings/', views.set_settings, name='set_priv'),
    path('accounts/profile/groups/', views.groups, name='groups'),
    url(r'^(?P<groupname>.+)/(?P<username>.+)/gropacc', views.grp_accept, name='grp_accept'),
    url(r'^(?P<groupname>.+)/(?P<username>.+)/gropdec', views.grp_decline, name='grp_decline'),
    url(r'^(?P<groupname>.+)/grp', views.group_box, name='group_box'),
    url(r'^(?P<groupname>.+)/grop_text', views.grp_send, name='grp_send'),
    path('grp_find', views.join_grp, name='join_grp'),
    url(r'^(?P<groupname>.+)/send_grp_req', views.user_to_grp, name='useradd'),
    path('grp_create', views.create_grp, name='create_grp'),
    path('accounts/profile/ewallet/wall_add/', views.TransactionView, name='OTP'),
    path('accounts/profile/ewallet/walletadd/', views.add_money, name='add_money'),

]
