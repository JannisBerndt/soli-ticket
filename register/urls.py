from django.urls import path
from .views import Register, error

urlpatterns = [
    path('', Register.as_view()),
    path('error/', error)
]
 
