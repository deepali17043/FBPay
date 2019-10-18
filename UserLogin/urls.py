from . import views
from django.urls import path
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    #   path('', views.LoginPage.as_view(), name ='login'),
    url(r'^login/', views.url_correction, name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/profile/', views.ProfileView, name='profile'),
    path('accounts/profile/options.html', views.OptionsView.as_view(), name='options'),
    path('accounts/profile/newsfeed.html', views.OptionsView.as_view(), name='newsfeed'),
    path('accounts/profile/notify.html', views.OptionsView.as_view(), name='notifications'),
    url(r'^(?P<username>.+)/ewallet', views.walletview, name='ewallet'),
    url(r'^(?P<username>.+)/accept', views.accept, name='accept'),
    url(r'^(?P<username>.+)/decline', views.walletview, name='decline'),
    url(r'^(?P<username>.+)/timeline', views.other_profile, name='other_user'),
    url(r'^(?P<username>.+)/send_req', views.addfriend, name='request'),
    url(r'^(?P<username>.+)/logoutuser/', views.logoutuser, name='logoutuser'),
    path('accounts/profile/FriendList.html', views.friends, name='F_list'),
    path('accounts/profile/find', views.find_friends, name='find_frd'),
    #   path('signup/',views.signup, name='new user')
]