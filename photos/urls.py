from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('view/<int:pk>', views.photo_view, name='photo_view'),
    path('new', views.photo_create, name='photo_new'),
    path('edit/<int:pk>', views.photo_update, name='photo_edit'),
    path('delete/<int:pk>', views.photo_delete, name='photo_delete'),
    url(r'^like/(?P<pic_id>\d+)/$', views.like_image, name='like'),
    url(r'^unlike/(?P<pic_id>\d+)/$', views.unlike_image, name='unlike'),
]