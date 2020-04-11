from django.urls import path
from .views import login_view, logout_view, profile_update_view, profile_delete_view, accounts, error_view, organiser_list_view, confirm_view, verify_email_view, profile_view
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from solisite.settings import EMAIL_HOST_USER

app_name='accounts'
urlpatterns = [
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('profile/edit/', profile_update_view, name='profile_update'),
    path('profile/delete/', profile_delete_view, name='profile_delete'),
    path('register/', accounts.as_view(), name='register'),
    path('error/', error_view, name='register_error'),
    path('organizer/', organiser_list_view, name='organiser_list'),
    path('confirm/', confirm_view, name="confirm"),
    path('verify/', verify_email_view, name="verify_email"),
    path('profile/<str:organiser>', profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='register/password_change.html', success_url=reverse_lazy('accounts:password_change_complete')), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='register/password_change_done.html'), name='password_change_complete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='register/request_password_reset.html',
                                                                 success_url=reverse_lazy('accounts:password_reset_done'),
                                                                 from_email=EMAIL_HOST_USER,
                                                                 email_template_name='register/password_reset_email.html',
                                                                 subject_template_name='register/password_reset_email_subject.txt'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='register/request_password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset.html', success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_done.html'), name='password_reset_complete'),
]
