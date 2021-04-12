from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField
from .apps import UsersConfig


class UserProfile(AbstractUser):
    fullName = models.CharField(max_length=20)
    description = models.TextField(max_length=40, blank=True)
    biography = models.CharField(max_length=80, blank=True)
    image = CloudinaryField('image')
    dateCreated = models.DateTimeField(auto_now_add=True)
    country = CountryField(default="IR")

    def save(self, *args, **kwargs):
        self.fullName = f'{self.first_name} {self.last_name}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


UsersConfig.default_auto_field = models.BigAutoField
