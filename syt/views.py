from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from photos.models import *
from comments.forms import CommentForm
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
@login_required(login_url='/users/login')
def index(request):
    following = request.user.following.values_list('following_id', flat=True)
    pics = Photo.objects.filter(user_id__in=following)
    pics |= Photo.objects.filter(user_id=request.user.id)
    pics = pics.order_by('-created_at')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user.id
            comment.pic_id = request.POST['pic']
            comment.save()
    form = CommentForm()
    data = {}
    data['photos'] = pics
    data['form'] = form
    if request.user.is_authenticated:
        liked = request.user.pic_likes.values_list('pic_id', flat=True)
        data['liked'] = list(liked)
    
    return render(request, 'index.html', data)

def explore(request):
    pics = Photo.objects.all().order_by('-created_at')
    data = {}
    data['photos'] = pics
    if request.user.is_authenticated:
        liked = request.user.pic_likes.values_list('pic_id', flat=True)
        data['liked'] = list(liked)
    
    return render(request, 'explore.html', data)

def profile(request, pk, template_name='users/profile.html'):
    pr_user = User.objects.get(pk=pk)
    following = request.user.following.filter(following_id=pk)
    total_following = request.user.following.values_list('following_id', flat=True)
    return render(request, template_name, {'pr_user': pr_user, 'following':following, 'total_following':total_following})