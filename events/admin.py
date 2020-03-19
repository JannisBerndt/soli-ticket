from django.contrib import admin

# Register your models here.
from .models import Buyable, Address, Event

admin.site.register(Event)
