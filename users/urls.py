from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('edit/<int:pk>', views.update, name='update_user'),
    url(r'^follow/(?P<user_id>\d+)/$', views.follow, name='follow'),
    url(r'^unfollow/(?P<fol_id>\d+)/$', views.unfollow, name='unfollow'),
]