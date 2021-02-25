from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'))),
    path('users/', include(('users.urls', 'users'))),
    path('gigs/', include(('gigs.urls', 'gigs'))),
    path('accounts/', include('allauth.urls')),
]
