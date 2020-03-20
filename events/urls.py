from django.contrib import admin
from django.urls import path

from .views import event_detail_view, event_list_view, event_create_view, event_update_view

app_name = "events"
urlpatterns = [
	path('', event_list_view, name='event_list'),
	path('<int:id>/', event_detail_view, name='event_detail'),
	path('create/', event_create_view, name='event_create'),
	path('<int:id>/update/', event_update_view, name='event_update'),
]