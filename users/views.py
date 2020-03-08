from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from followers.models import *
from django.http import HttpResponseRedirect
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

def register(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password']
            password2 = request.POST['password_confirmation']
            email = request.POST['email']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Already Taken!!')
                    return redirect('/users/register') 
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Taken!!')
                    return redirect('users/register') 
                else:
                    user = User.objects.create_user(first_name=first_name, password=password1, email=email, last_name=last_name, username=username)
                    user.save()
                    auth.login(request, user)
                    messages.info(request, 'User Created!!')
                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching!!')
                return redirect('users/register')  
        else:   
            return render(request, 'users/register.html')

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

