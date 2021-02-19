from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class UserProfile(AbstractUser):
    short_bio = models.CharField("write short bio", max_length=35, default=' ')
    description = models.TextField("long description", default=' ')
    date_joined = models.DateTimeField(auto_now_add=True)
    country = CountryField(default="IR")
    full_name = models.CharField("full name", max_length=20, blank=True)


    def save(self, *args, **kwargs):
        self.full_name = self.first_name + self.last_name
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.username
