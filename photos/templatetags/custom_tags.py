from django import template
from photos.models import *
from likes.models import *
from followers.models import *
from comments.models import *
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def total_likes(photo_id):
    return Like.objects.filter(pic_id = photo_id).count()

@register.simple_tag
def total_followers(user_id):
    return User.objects.get(pk=user_id).followers.all().count()

@register.simple_tag
def pic_comments(pic_id):
    return Comment.objects.filter(pic_id=pic_id)
