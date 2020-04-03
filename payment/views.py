from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from events.models import Buyable
from accounts.models import Order

# Create your views here.

def payment_process(request):
	invoiceUID = request.session["invoiceUID"]
	sum = request.session["sum"]
	paypal_email = request.session["paypal_email"]
	
	if settings.PAYPAL_TEST:
		paypal_email = settings.PAYPAL_RECEIVER_EMAIL
	
	host = settings.HOST_URL_BASE

	orders = Order.objects.filter(invoiceUID = invoiceUID)
	
	if orders is None:
		return Exception
	
	amount = sum/1.19
	tax = amount*0.19

	paypal_dict = {
		'business': paypal_email,
		'amount': '%.2f' % amount,
		'tax': '%.2f' % tax,
		'invoice': str(invoiceUID),
		'currency_code': 'EUR',
		'notify_url': '{host_base_url}payment/notify/'.format(host_base_url = host),
		'return_url': '{host_base_url}payment/done/'.format(host_base_url = host),
		'cancel_return': '{host_base_url}payment/canceled/'.format(host_base_url = host),
	}

	i = 1
	
	paypal_dict['cmd'] = '_cart'
	paypal_dict['upload'] = 1

	paypal_dict['item_name_1'] = 'Cola'
	paypal_dict['item_name_2'] = 'Eintrittskarte'
	paypal_dict['tax_1'] = 0.5
	paypal_dict['tax_2'] = 0.7
	paypal_dict['amount_1'] = 1.00
	paypal_dict['amount_2'] = 1.00
	paypal_dict['quantity_1'] = 1
	paypal_dict['quantity_2'] = 3
	paypal_dict['submit'] = 'PayPal'
	paypal_dict['shipping_1'] = 4.00
	paypal_dict['shipping_2'] = 8.00

	"""
	for order in orders:
		
		platzhalter = 'item_name_'+str(i)
		buyable = Buyable.objects.get(id = order.article_id)
		wert = buyable.buyable_name
		paypal_dict[platzhalter] = wert
		i+=1
	"""
	
	form = PayPalPaymentsForm(initial=paypal_dict)
	print(form)
	return render(request, 'payment/process.html', {'form': form,})

@csrf_exempt
def payment_done(request):
	return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment/canceled.html')

