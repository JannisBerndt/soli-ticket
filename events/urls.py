from django.urls import path
from .views import event_detail_view, event_create_view, event_update_view, event_delete_view, profile_redirect

app_name = "events"
urlpatterns = [
	path('create/', event_create_view, name='event_create'),
	path('<int:id>/', event_detail_view, name='event_detail'),
	path('<int:id>/edit/', event_update_view, name='event_update'),
	path('<int:id>/delete/', event_delete_view, name='event_delete'),
	path('<str:organiser>/', profile_redirect, name='profile_redirect'),
]
