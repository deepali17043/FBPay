from . import views
from django.urls import path
from django.urls import path, include

urlpatterns = [
    #   path('', views.LoginPage.as_view(), name ='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/options.html', views.OptionsView.as_view(), name='options'),
    path('accounts/profile/newsfeed.html', views.OptionsView.as_view(), name='newsfeed'),
    path('accounts/profile/notify.html', views.OptionsView.as_view(), name='notifications'),
    #   path('signup/',views.signup, name='new user')
]