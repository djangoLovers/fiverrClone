from django.urls import path
from .views import index, show, edit

urlpatterns = [
    path('', index, name='index'),
    path('<int:id>/', show, name='show'),
    path('<int:id>/edit/', edit, name='edit')
]
