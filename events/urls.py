from django.contrib import admin
from django.urls import path

from .views import event_detail_view, event_create_view, event_update_view, event_delete_view, buyable_create_view, buyable_update_view,buyable_delete_view, event_organiser_list_view

app_name = "events"
urlpatterns = [
	# path('', event_list_view, name='event_list'),
	path('create/', event_create_view, name='event_create'),
	path('<int:id>/', event_detail_view, name='event_detail'),
	# path('<int:id>/checkout/', checkout_view, name='checkout'),
	#path('<int:id>/update/', event_update_view, name='event_update'),
	path('<int:id>/delete/', event_delete_view, name='event_delete'),
	#path('<int:id>/buyable/create/', buyable_create_view, name='buyable_create'),
	#path('<int:id_e>/buyable/<int:id_b>/update/', buyable_update_view, name='buyable_update'),
	#path('<int:id_e>/buyable/<int:id_b>/delete/', buyable_delete_view, name='buyable_delete'),
	path('<str:organiser>/', event_organiser_list_view, name='event_organiser_list'),
]
