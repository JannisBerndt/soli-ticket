from django.contrib import admin
from django.urls import path

from .views import event_detail_view

app_name = "events"
urlpatterns = [
	path('<int:id>/', event_detail_view, name='event_detail')
]