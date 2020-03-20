from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_start, name='start'),
    path('detail/', views.register_detail, name='detail'),
    path('profile/<str:pk>', views.profile, name='profile'),
]
