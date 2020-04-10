from django.urls import path, include
from .views import login_view, logout_view, profile_update_view, profile_delete_view, accounts, error_view, organiser_list_view, confirm_view, profile_view

app_name='accounts'
urlpatterns = [
    path('login/', login_view, name ='login'),
    path('logout/', logout_view, name ='logout'),
    path('profile/edit/', profile_update_view, name='profile_update'),
    path('profile/delete/', profile_delete_view, name='profile_delete'),
    path('profile/<str:organiser>/', profile_view, name='profile'),
    path('profile/<str:organiser>/event/', include('events.urls')),
    path('register/', accounts.as_view(), name='register'),
    path('error/', error_view, name='register_error'),
    path('organizer/', organiser_list_view, name='organiser_list'),
    path('confirm/', confirm_view, name='confirm'),
]
