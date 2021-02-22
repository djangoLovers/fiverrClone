from django.urls import path
from .views import index, show, new, edit, PaymentView, PaymentCallbackView


urlpatterns = [
    path('', index, name='index'),
    path('<int:id>/', show, name='show'),
    path('new/', new, name='new'),
    path('<int:id>/edit/', edit, name='edit'),


    path(r'<int:id>/order/^$', PaymentView.as_view(), name='payment'),
    path('callback/',
         PaymentCallbackView.as_view(), name='payment_callback'),
]
