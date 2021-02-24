from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.conf import settings


class UserProfile(AbstractUser):
    fullName = models.CharField(max_length=20)
    description = models.TextField(max_length=40, blank=True)
    biography = models.CharField(max_length=80, blank=True)
    image = models.ImageField(null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    country = CountryField(default="IR")

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            #make sure to have an image named user_default in statics/images
            return "%s/user_default.jpg" % settings.MEDIA_URL


    def save(self, *args, **kwargs):
        self.fullName = f'{self.first_name} {self.last_name}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username
