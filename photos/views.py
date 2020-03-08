from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.models import User, auth
from .models import Photo
from .forms import *
from likes.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/login')
def photo_list(request, template_name='photos/photo_list.html'):
    images = request.user.photos.all()
    liked = request.user.pic_likes.values_list('pic_id', flat=True)
    data = {}
    data['object_list'] = images
    data['liked'] = list(liked)
    return render(request, template_name, data)

def photo_view(request, pk, template_name='photos/photo_detail.html'):
    image = get_object_or_404(Photo, pk=pk)
    liked = Like.objects.filter(pic_id = image.id, user_id=request.user.id).exists()
    return render(request, template_name, {'object':image, 'liked': liked})

def photo_create(request, template_name='photos/photo_form.html'):
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('photo_list')
    return render(request, template_name, {'form':form})

def photo_update(request, pk, template_name='photos/photo_form.html'):
    image = get_object_or_404(Photo, pk=pk)
    form = PhotoForm(request.POST, request.FILES, instance=image)
    if form.is_valid():
        form.save()
        return redirect('photo_list')
    return render(request, template_name, {'form':form})

def photo_delete(request, pk, template_name='photos/photo_confirm_delete.html'):
    image = get_object_or_404(Photo, pk=pk)    
    if request.method=='POST':
        image.delete()
        return redirect('photo_list')
    return render(request, template_name, {'object':image})

def like_image(request, pic_id):
    pic = Photo.objects.filter(pk=pic_id)[0]
    Like.objects.create(user=request.user, pic=pic)
    return redirect('/images')

def unlike_image(request, pic_id):
    like = Like.objects.get(pic_id=pic_id, user_id= request.user.id)
    like.delete()
    return redirect('/images')