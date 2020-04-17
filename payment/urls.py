from django.urls import path
from .views import payment_canceled_view, payment_done_view, payment_process_view, payment_ipn_view

app_name = "payment"
urlpatterns = [
	path('done/', payment_done_view, name='done'),
	path('canceled/', payment_canceled_view, name='canceled'),
	path('process/', payment_process_view, name='process'),
	path('notify/', payment_ipn_view, name='ipn'),
]
