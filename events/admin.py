from django.contrib import admin

# Register your models here.
from .models import Event, Address, Buyable

admin.site.register(Event)
admin.site.register(Address)
admin.site.register(Buyable)