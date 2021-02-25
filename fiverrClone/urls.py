from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'))),
    path('users/', include(('users.urls', 'users'))),
    path('gigs/', include(('gigs.urls', 'gigs'))),
    path('accounts/', include('allauth.urls')),
]

if not settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            )
