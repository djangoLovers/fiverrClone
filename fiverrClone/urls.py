from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'))),
    path('users/', include(('users.urls', 'users'))),
    path('accounts/', include('allauth.urls')),

]
