from django.contrib import admin
from django.urls import path

from .views import event_detail_view, event_create_view, event_update_view, event_delete_view, event_organiser_list_view

app_name = "events"
urlpatterns = [
	path('create/', event_create_view, name='event_create'),
	path('<int:id>/', event_detail_view, name='event_detail'),
	# path('<int:id>/checkout/', checkout_view, name='checkout'),
	path('<int:id>/edit/', event_update_view, name='event_update'),
	path('<int:id>/delete/', event_delete_view, name='event_delete'),
	path('<str:organiser>/', event_organiser_list_view, name='event_organiser_list'),
]
