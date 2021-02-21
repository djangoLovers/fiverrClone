from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

# Create your models here.
class Gig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="gigs")
    title = models.CharField("Gig title", max_length=80, blank=False)
    price = models.IntegerField("Gig price", null=False, blank=False)
    description = models.TextField("Describe the gig")
    categories  = models.ManyToManyField(Categories)
    created_date = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    name = models.CharField("Name", max_length=15, blank=False)


class Review(models.Model);
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="gigs")
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    content = models.CharField(max_length=200, blank=False)
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="gigs")
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name="orders")
    created_date = models.DateTimeField(auto_now_add=True)
