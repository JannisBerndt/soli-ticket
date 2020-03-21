from django.urls import path
from .views import accounts, error

urlpatterns = [
    path('', accounts.as_view()),
    path('error/', error)
]
 
