from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_start),
    path('detail/', views.register_detail, name='detail'),
]
