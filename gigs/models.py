from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model

UserProfile = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Gig(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=CASCADE, blank=True)
    name = models.CharField(max_length=90)
    dateCreated = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = ForeignKey(UserProfile, on_delete=CASCADE)
    gig = ForeignKey(Gig, on_delete=CASCADE)
    body = models.CharField(max_length=255)
    rating = models.IntegerField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.gig} - {self.user} - {self.rating}'


class Order(models.Model):
    user = ForeignKey(UserProfile, on_delete=CASCADE)
    gig = ForeignKey(Gig, on_delete=CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.gig} - {self.user}'
