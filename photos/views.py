from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.models import User, auth
from .models import Photo
from .forms import *
from comments.models import Comment
from comments.forms import CommentForm
from likes.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

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
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user.id
            comment.pic_id = pk
            comment.save()
    form = CommentForm()
    liked = Like.objects.filter(pic_id = image.id, user_id=request.user.id).exists()
    comments = image.comments.all
    is_owner = (image.user.id == request.user.id)
    return render(request, template_name, {'object':image, 'liked': liked, 'comments':comments, 'form':form, 'is_owner': is_owner})

def photo_create(request, template_name='photos/photo_form.html'):
    data = request.POST
    data._mutable = True
    data['user'] = str(request.user.id)
    data._mutable = False
    form = PhotoForm(data, request.FILES, hide_condition=True)
    import pdb; pdb.set_trace()
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

@login_required(login_url='/users/login')
def photo_delete(request, pk, template_name='photos/photo_confirm_delete.html'):
    image = get_object_or_404(Photo, pk=pk)
    if (image.user.id == request.user.id):   
        if request.method=='POST':
            image.delete()
            return redirect('photo_list')
        return render(request, template_name, {'object':image})
    else:
        messages.error(request, 'You are not authorised to delete this pic.')
        return redirect('/p')

def like_image(request, pic_id):
    pic = Photo.objects.filter(pk=pic_id)[0]
    Like.objects.create(user=request.user, pic=pic)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def unlike_image(request, pic_id):
    like = Like.objects.get(pic_id=pic_id, user_id= request.user.id)
    like.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))