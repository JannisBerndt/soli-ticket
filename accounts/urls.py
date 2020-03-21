from django.urls import path
from .views import accounts, error

urlpatterns = [
    path('register/', accounts.as_view(), name='register'),
    path('error/', error, name='register_error')
]
