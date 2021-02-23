from django.urls import path
from .views import index, show, new, edit, comment, order, callback, result


urlpatterns = [
    path('', index, name='index'),
    path('<int:id>/', show, name='show'),
    path('new/', new, name='new'),
    path('<int:id>/edit/', edit, name='edit'),
    path('<int:id>/comment/', comment, name='comment'),
    path('<int:id>/order/', order, name='order'),
    path('callback/', callback, name='callback'),
    path('result/', result, name='result')
]
