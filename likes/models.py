from django.db import models
from django.contrib.auth.models import User
from photos.models import *
from django.conf import settings

class Like(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pic_likes')
    pic= models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    date= models.DateTimeField(auto_now= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user) + ' liked photo id' + str(self.pic.id)

    class Meta:
       unique_together = ("user", "pic")
