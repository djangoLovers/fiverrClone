from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path('<int:pk>/update', views.user_update_view, name='update'),
    path('<str:full_name>', views.user_detail_view, name='detail'),
]