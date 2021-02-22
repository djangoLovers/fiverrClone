from django.urls import path
from .views import index, show, edit, my_orders, my_purchases

urlpatterns = [
    path('', index, name='index'),
    path('<int:id>/', show, name='show'),
    path('<int:id>/edit/', edit, name='edit'),
    path('orders/', my_orders, name="orders"),
    path('purchases/', my_purchases, name="purchases")
]
