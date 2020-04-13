from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from .views import payment_canceled, payment_done, payment_process, payment_ipn, payment_stripe

app_name = "payment"
urlpatterns = [
	path('done/', payment_done, name='done'),
	path('canceled/', payment_canceled, name='canceled'),
	path('process/', payment_process, name='process'),
	path('stripe/', payment_stripe, name='stripe'),
	path('notify/', payment_ipn, name='ipn'),
]