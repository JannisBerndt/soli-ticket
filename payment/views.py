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
	host = request.get_host

	paypal_dict = {
		'business': paypal_email,
		'amount': '%.2f' % sum,
		'item_name': 'Spende über Soli-Ticket.de',
		'invoice': str(order_id),
		'currency_code': 'EUR',
		'notify_url': 'http://{}/payment/notify/'.format(host),
		'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
		'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
	}

	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html', {'order_id': order_id, 'form': form,})

@csrf_exempt
def payment_done(request):
	return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment/canceled.html')