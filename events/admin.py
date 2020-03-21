from django.contrib import admin

# Register your models here.
from .models import Event, Eventlocation, Buyable

admin.site.register(Event)
admin.site.register(Eventlocation)
admin.site.register(Buyable)