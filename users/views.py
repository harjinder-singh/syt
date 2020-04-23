from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import auth
from followers.models import *
from .models import CustomUser
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer
User = get_user_model()
#from django.contrib.auth.decorators import login_required

def index(request):
    all_users = User.objects.filter(is_staff=False)
    following = Follower.objects.filter(follower_id = request.user.id).values_list('following_id', flat=True)
    following = list(following)
    if request.user.is_authenticated:
        followers_count = request.user.followers.all().count()
        return render(request, 'users/index.html',{'all_users':all_users, 'followers_count' : followers_count, 'following': following})
    else:
        return render(request, 'users/index.html',{'all_users':all_users, 'following': following})

def register(request, template_name='users/register.html'):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if form.is_valid():
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username Already Taken!!')
                        return redirect('/users/register') 
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Already Taken!!')
                        return redirect('users/register') 
                    else:
                        form.save()
                        messages.info(request, 'Account Created!! Please login to upload your first pic.')
                        return redirect('/')
                else:
                    messages.info(request, 'Password Not Matching!!')
                    return redirect('users/register')  
            else:
                messages.info(request, 'There is some error processing your information. Please try again!!')
                return redirect('users/register')
        else:
            return render(request, template_name, {'form':form})  

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Login failed!!')
                return redirect('login') 
        else:   
            return render(request, 'users/login.html')

def update(request, pk, template_name='users/edit.html'):
    user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile Updated Successfully!!')
            return redirect('/'+str(user.id))
        else:
            messages.info(request, 'There is some error processing your information. Please try again!!' + str(form.errors))
            return redirect(str(user.id))
    return render(request, template_name, {'form':form})

def logout(request):
    
    auth.logout(request)
    return redirect('/')

def follow(request, user_id):

    Follower.objects.create(follower=request.user, following=User.objects.filter(pk = user_id)[0])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def unfollow(request, fol_id):

    fol = Follower.objects.get(pk=fol_id)
    fol.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class ListUsersView(generics.ListAPIView):

    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

