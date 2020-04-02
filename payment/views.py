from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.

def payment_process(request):
	order_id = request.session["order_id"]
	sum = request.session["sum"]
	paypal_email = request.session["paypal_email"]
	if settings.PAYPAL_TEST:
		paypal_email = settings.PAYPAL_RECEIVER_EMAIL
	
	host = settings.HOST_URL_BASE

	amount = sum/1.19
	tax = amount*0.19

	paypal_dict = {
		'business': paypal_email,
		'amount': '%.2f' % amount,
		'tax': '%.2f' % tax,
		'item_name': 'Zahlung über Soli-Ticket.de',
		'invoice': str(order_id),
		'currency_code': 'EUR',
		'notify_url': '{host_base_url}payment/notify/'.format(host_base_url = host),
		'return_url': '{host_base_url}payment/done/'.format(host_base_url = host),
		'cancel_return': '{host_base_url}payment/canceled/'.format(host_base_url = host),
	}

	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html', {'order_id': order_id, 'form': form,})

@csrf_exempt
def payment_done(request):
	return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment/canceled.html')