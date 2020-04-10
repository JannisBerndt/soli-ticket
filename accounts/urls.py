from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('profile/edit/', views.profile_update_view, name='profile_update'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('register/', views.accounts.as_view(), name='register'),
    path('error/', views.error, name='register_error'),
    path('organizer/', views.organiser_list_view, name='organiser_list'),
    path('confirm/', views.confirm),
    path('verify/', views.verify_email_view, name="verify_email"),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='register/password_change.html', success_url=reverse_lazy('accounts:profile_update')), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='register/password_change_done.html'), name='password_change_complete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='register/request_password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_done.html'), name='password_reset_complete'),
]
