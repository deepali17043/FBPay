from . import views
from django.urls import path
from django.urls import path, include


urlpatterns =[
 #   path('', views.LoginPage.as_view(), name ='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile')
 #   path('signup/',views.signup, name='new user')
]