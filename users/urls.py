from django.urls import path
from .views import show, edit, orders, sales

urlpatterns = [
    path('<int:id>/', show, name='show'),
    path('<int:id>/edit/', edit, name='edit'),
    path('<int:id>/orders/', orders, name="orders"),
    path('<int:id>/sales/', sales, name="sales")
]
