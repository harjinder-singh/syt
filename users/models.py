from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    description = models.TextField(max_length=50)
    pic = models.ImageField(upload_to='user_profile_pics')

    def __str__(self):
        return self.username