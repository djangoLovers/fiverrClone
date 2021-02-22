from django.urls import path
from .views import callback, index, show, new, edit, order


urlpatterns = [
    path('', index, name='index'),
    path('<int:id>/', show, name='show'),
    path('new/', new, name='new'),
    path('<int:id>/edit/', edit, name='edit'),
    path('<int:id>/order/', order, name='order')
]
