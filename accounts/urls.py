from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    # path('profile/', views.profile, name='profile'),
    path('register/', views.accounts.as_view(), name='register'),
    path('error/', views.error, name='register_error'),
    path('organizer/', views.organiser_list_view, name='organiser_list'),
]
