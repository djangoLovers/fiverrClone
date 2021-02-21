from django.contrib import admin
from users.models import UserProfile
from gigs.models import Gig, Order, Comment, Category

admin.site.register(UserProfile)
admin.site.register(Gig)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Category)
