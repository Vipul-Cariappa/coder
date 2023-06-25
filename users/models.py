import os
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from PIL import Image


# Create your models here.
class UserProfile(models.Model):
    biography = models.TextField(max_length=500, default="My Bio")
    picture = models.ImageField(upload_to="images/", default="default.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self):
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
