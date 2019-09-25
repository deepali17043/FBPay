from . import views
from django.urls import path


urlpatterns =[
    path('', views.LoginPage.as_view(), name='login')
]