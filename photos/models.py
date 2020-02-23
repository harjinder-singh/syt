from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Photo(models.Model):
    description = models.TextField(max_length=50)
    pic = models.ImageField(upload_to='pics')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('image_edit', kwargs={'pk': self.pk})
