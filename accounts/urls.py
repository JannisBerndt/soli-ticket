from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('register/', views.accounts.as_view(), name='register'),
    path('error/', views.error, name='register_error')
]
