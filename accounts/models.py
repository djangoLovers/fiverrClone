from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    pass

    def __str__(self) -> str:
        return self.username
