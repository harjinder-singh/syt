from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from photos.models import *
User = get_user_model()

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.id},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def listUsers(request):
    data = User.objects.filter(is_staff=False).values('username', 'first_name', 'last_name', 'email')
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def listimages(request):
    all_images = Photo.objects.all()
    user_ids = all_images.values_list('user', flat=True)
    users = User.objects.filter(id__in=user_ids).values('id', 'username', 'pic')
    images = all_images.values("id","user", "description", "pic", "created_at", "updated_at")
    data = {"users": users, "images": images}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def profile(request):
    followers = request.user.followers.values("id","follower", "following", "created_at", "updated_at")
    following = request.user.following.values("id","follower", "following", "created_at", "updated_at")
    data = {"following": following, "followers": followers}
    return Response(data, status=HTTP_200_OK)