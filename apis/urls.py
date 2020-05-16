from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('users', views.listUsers),
    path('login', views.login),
    path('images', views.listimages),
    path('profile', views.profile)
]