from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class UserProfile(AbstractUser):
    short_bio = models.CharField("write short bio", max_length=35)
    description = models.TextField("long description")
    date_joined = models.DateTimeField(auto_now_add=True)
    country = CountryField()


    def __str__(self) -> str:
        return self.username
