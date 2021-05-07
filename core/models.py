from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField


class UserProfile(AbstractUser):
    fullName = models.CharField(max_length=20)
    description = models.TextField(max_length=40, blank=True)
    biography = models.CharField(max_length=80, blank=True)
    image = CloudinaryField('image')
    dateCreated = models.DateTimeField(auto_now_add=True)
    country = CountryField(default="IR")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.fullName = f'{self.first_name} {self.last_name}'
        return super().save(*args, **kwargs)


class GigQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query)
            )
            qs = self.filter(or_lookup).distinct()
        return qs


class GigManager(models.Manager):
    def get_queryset(self):
        return GigQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Gig(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, related_name="gigs_user")
    name = models.CharField(max_length=90)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=90, null=True)
    quantity = models.IntegerField(default=0)
    image = CloudinaryField('image', blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name="gigs_category")

    objects = GigManager()

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="comments_user")
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE,
                            related_name="comments_gig")
    body = models.CharField(max_length=255)
    rating = models.IntegerField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.gig} - {self.user} - {self.rating}'


class Order(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="orders_user")
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE,
                            related_name="orders_gig")
    delivered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.gig} - {self.user}'
