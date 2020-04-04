from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from events.models import Buyable
from accounts.models import Order, UserAddress
from django.db.models.query import RawQuerySet







# Nur um zu testen....
from django.core.mail import send_mail
import logging
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from paypal.standard.ipn.forms import PayPalIPNForm
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.models import DEFAULT_ENCODING
from paypal.utils import warn_untested

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



CONTENT_TYPE_ERROR = ("Invalid Content-Type - PayPal is only expected to use "
                      "application/x-www-form-urlencoded. If using django's "
                      "test Client, set `content_type` explicitly")
logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def payment_ipn(request):
    """
    PayPal IPN endpoint (notify_url).
    Used by both PayPal Payments Pro and Payments Standard to confirm transactions.
    http://tinyurl.com/d9vu9d

    PayPal IPN Simulator:
    https://developer.paypal.com/cgi-bin/devscr?cmd=_ipn-link-session
    """
    # TODO: Clean up code so that we don't need to set None here and have a lot
    #       of if checks just to determine if flag is set.
    flag = None
    ipn_obj = None

    # Avoid the RawPostDataException. See original issue for details:
    # https://github.com/spookylukey/django-paypal/issues/79
    if not request.META.get('CONTENT_TYPE', '').startswith(
            'application/x-www-form-urlencoded'):
        raise AssertionError(CONTENT_TYPE_ERROR)



    # Clean up the data as PayPal sends some weird values such as "N/A"
    # Also, need to cope with custom encoding, which is stored in the body (!).
    # Assuming the tolerant parsing of QueryDict and an ASCII-like encoding,
    # such as windows-1252, latin1 or UTF8, the following will work:
    encoding = request.POST.get('charset', None)

    encoding_missing = encoding is None
    if encoding_missing:
        encoding = DEFAULT_ENCODING

    try:
        data = QueryDict(request.body, encoding=encoding).copy()
    except LookupError:
        warn_untested()
        data = None
        flag = "Invalid form - invalid charset"

    if data is not None:
        if hasattr(PayPalIPN._meta, 'get_fields'):
            date_fields = [f.attname for f in PayPalIPN._meta.get_fields() if f.__class__.__name__ == 'DateTimeField']
        else:
            date_fields = [f.attname for f, m in PayPalIPN._meta.get_fields_with_model()
                           if f.__class__.__name__ == 'DateTimeField']

        for date_field in date_fields:
            if data.get(date_field) == 'N/A':
                del data[date_field]

        form = PayPalIPNForm(data)
        if form.is_valid():
            try:
                # When commit = False, object is returned without saving to DB.
                ipn_obj = form.save(commit=False)
            except Exception as e:
                flag = "Exception while processing. (%s)" % e
        else:
            formatted_form_errors = ["{0}: {1}".format(k, ", ".join(v)) for k, v in form.errors.items()]
            flag = "Invalid form. ({0})".format(", ".join(formatted_form_errors))

    if ipn_obj is None:
        ipn_obj = PayPalIPN()

    # Set query params and sender's IP address
    ipn_obj.initialize(request)

    if flag is not None:
        # We save errors in the flag field
        ipn_obj.set_flag(flag)
    else:
        # Secrets should only be used over SSL.
        if request.is_secure() and 'secret' in request.GET:
            warn_untested()
            ipn_obj.verify_secret(form, request.GET['secret'])
        else:
            ipn_obj.verify()


    subject='Bestätigung'
    content='Jo, Zahlung mit folgender invoice-URL erhalten {invoiceUID}'.format(invoiceUID = ipn_obj.invoice)
    send_mail(subject, content, settings.EMAIL_HOST_USER, ['roessler.paul@web.de'])
    ipn_obj.save()
    ipn_obj.send_signals()

    if encoding_missing:
        # Wait until we have an ID to log warning
        logger.warning("No charset passed with PayPalIPN: %s. Guessing %s", ipn_obj.id, encoding)

    return HttpResponse("OKAY")

