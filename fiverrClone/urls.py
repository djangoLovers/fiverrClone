from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('fiverradmin/', admin.site.urls),
    path('', include(('core.urls', 'core'))),
    path('users/', include(('users.urls', 'users'))),
    path('gigs/', include(('gigs.urls', 'gigs'))),
    path('accounts/', include('allauth.urls'))
]
