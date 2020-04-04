from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from events.models import Buyable
from accounts.models import Order, UserAddress
from django.db.models.query import RawQuerySet

# Create your views here.

def payment_process(request):
	invoiceUID = request.session["invoiceUID"]
	paypal_email = request.session["paypal_email"]
	
	if settings.PAYPAL_TEST:
		paypal_email = settings.PAYPAL_RECEIVER_EMAIL
	
	host = settings.HOST_URL_BASE

	orders = Order.objects.filter(invoiceUID = invoiceUID)
	
	if orders is None:
		return Exception

	"""
	sql = 'SELECT au.id, strasse, hnummer, plz, ort FROM accounts_useraddress AS au INNER JOIN auth_user AS auu ON au.id = auu.id INNER JOIN events_buyable AS eb ON eb.creator_id = auu.id INNER JOIN accounts_order AS ao ON eb.id = ao.article_id WHERE ao.invoiceUID = %s'
	o_adresse = UserAddress.objects.raw(sql, [invoiceUID])[0]

	hnummer = o_adresse.hnummer
	strasse = o_adresse.strasse
	ort = o_adresse.ort
	plz = o_adresse.plz
	
	print(hnummer + '\n' + strasse + '\n' + ort + '\n' + plz)
	"""

	paypal_dict = {
		'cmd':'_cart',
		'upload':1,
		'business': paypal_email,
		'invoice': str(invoiceUID),
		'currency_code': 'EUR',
		'notify_url': '{host_base_url}payment/notify/'.format(host_base_url = host),
		'return_url': '{host_base_url}payment/done/'.format(host_base_url = host),
		'cancel_return': '{host_base_url}payment/canceled/'.format(host_base_url = host),
		'submit':'PayPal',
		'custom':'DAS ist die Info im Custom-Feld'
	}


	i = 1
	for order in orders:
		itemNamePlatzhalter = 'item_name_'+str(i)
		steuerWertPlatzhalter = 'tax_'+str(i)
		itemAnzahlPlatzhalter = 'quantity_'+str(i)
		itemPreisPlatzhalter = 'amount_'+str(i)

		article_id = order.article_id
		article = Buyable.objects.get(id = article_id)

		tax_rate = article.tax_rate

		itemName = article.buyable_name
		itemPreis = article.price/(1+tax_rate)
		itemSteuer = itemPreis * tax_rate
		itemAnzahl = order.amount

		paypal_dict[itemNamePlatzhalter] = itemName
		paypal_dict[steuerWertPlatzhalter] = itemSteuer
		paypal_dict[itemAnzahlPlatzhalter] = itemAnzahl
		paypal_dict[itemPreisPlatzhalter] = itemPreis

		i+=1

	"""
	paypal_dict['item_name_1'] = 'Cola'
	paypal_dict['item_name_2'] = 'Eintrittskarte'
	paypal_dict['tax_1'] = 0.5
	paypal_dict['tax_2'] = 0.7
	paypal_dict['amount_1'] = 1.00
	paypal_dict['amount_2'] = 1.00
	paypal_dict['quantity_1'] = 1
	paypal_dict['quantity_2'] = 3

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

