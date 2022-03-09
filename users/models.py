# from django.contrib.auth import get_user_model as user_model
from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.db import models

# User = user_model()


class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to="static/img/admin_profile_images", null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
