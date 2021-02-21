from django.contrib import admin
from .models import Gig, Order, Comment, Category


admin.site.register(Gig)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Category)
