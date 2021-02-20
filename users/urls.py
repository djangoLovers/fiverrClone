from django.urls import path
from .views import index, edit

urlpatterns = [
    path('', index, name='index'),
    path('edit/', edit, name='edit')
]
