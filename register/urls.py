from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list),
    path('register/', views.register_start),
]
