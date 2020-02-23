from django.shortcuts import render
from photos.models import *

# Create your views here.
def index(request):
    pics = Photo.objects.all()
    data = {}
    data['photos'] = pics
    if request.user.is_authenticated:
        liked = request.user.pic_likes.values_list('pic_id', flat=True)
        data['liked'] = list(liked)
    
    return render(request, 'index.html', data)

def profile(request, pk, template_name='users/profile.html'):
    pr_user = User.objects.get(pk=pk)
    following = request.user.following.filter(following_id=pk)
    return render(request, template_name, {'pr_user': pr_user, 'following':following})