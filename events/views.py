from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from accounts.models import Organiser, Customer, Order
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django import forms
from decimal import Decimal
from .models import Event, Eventlocation, Buyable
from .forms import EventForm, EventlocationForm, BuyableForm, BuyableFormSet, BuyableInlineFormSet, BuyableModelFormSet, validate_with_initial
from accounts.forms import OrderForm
import uuid 
import random
import string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pdb

def event_detail_view(request, id):
	event = get_object_or_404(Event, id=id)
	organiser = Organiser.objects.get(organisation_name=event.creator.organisation_name)

	
	print(organiser)
	try:
		organiser_user = Organiser.objects.get(username = request.user.username)
	except:
		organiser_user = None
	buyables = Buyable.objects.filter(belonging_event=event)
	location = event.location
	OrderFormSet = inlineformset_factory(Customer, Order, form=OrderForm, fields=['amount',], extra=buyables.count())
	order_formset = OrderFormSet(queryset=Order.objects.none())

	if request.method == 'POST':
		try:
			customer = Customer.objects.get(username=request.user.username)
		except:
			customer = None

		order_formset = OrderFormSet(request.POST, instance=customer)

	
		o_Event = Event.objects.get(id = id)
		o_Organisation = Organiser.objects.get(id = o_Event.creator_id)

		if not o_Organisation.paypal_email:
			return render(request, 'event/error.html')

		if order_formset.is_valid():
			i=0
			sum = 0
			orders = []
			
			# Neue RechnungsUID wird generiert und es werden sich Orders, die dazu bereits in der DB existieren geholt
			o_uid = invoiceUID_generator()
			o_orders = Order.objects.filter(invoiceUID = o_uid)
		
			#Sollten schon Orders dazu existieren, wird solange eine neue UID erzeugt und die Daten geholt, bis des Queryset o_orders leer ist.
			while o_orders:
				o_uid = invoiceUID_generator()
				o_orders = Order.objects.filter(invoiceUID = o_uid)

			for order_form in order_formset:
				order = order_form.save(commit=False)
				if order.amount:
					order.article = buyables[i]
					order.price = buyables[i].price * order.amount
					order.customer = customer
					order.customer_mail = request.POST.get('field-4')
					order.invoiceUID = o_uid
					order.save()
					sum += order.price
					orders.append(order)
				i += 1
			sum = float(sum)
			if orders:
				organiser = event.creator
				context = {
					'sum': sum,
					'organiser': organiser,
					'orders': orders,
					'event': event,
					'authenticated': request.user.is_authenticated,
					'organiser_user': organiser_user,
				}

				if organiser.paypal_email:
					request.session["invoiceUID"] = o_uid
					request.session["sum"] = sum
					request.session["paypal_email"] = organiser.paypal_email
					return redirect(reverse('payment:process'))
				

	formset = zip(buyables, order_formset)
	context = {
		'event': event,
		'buyables': buyables,
		'location': location,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
		'order_formset': order_formset,
		'formset': formset,
		'organiser_user': organiser_user,
		'organiser': organiser,
	}
	return render(request, "event/event_detail.html", context)

# def checkout_view(request, id):
# 	event = Event.objects.get(id=id)
# 	organiser = event.creator
# 	customer = Customer.objects.get(username='default')
# 	orders = customer.customer_set.all()
# 	sum = 0
# 	for order in orders:
# 		sum += order.price
# 	context = {
# 		'sum': sum,
# 		'organiser': organiser,
# 		'orders': orders,
# 		'event': event,
# 		'authenticated': request.user.is_authenticated,
# 	}
# 	return render(request, "event/event_donate.html", context)

@login_required(login_url='accounts:login')
def event_create_view(request):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	if organiser.organisation_type == 'gemeinnützig':
		initial_data = [{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},]
	else:
		initial_data = [{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},]
	if request.method == 'POST':
		event_form = EventForm(request.POST)
		location_form = EventlocationForm(request.POST)
		buyable_formset = BuyableModelFormSet(request.POST, queryset=Buyable.objects.none(), initial = initial_data)
		if event_form.is_valid() and location_form.is_valid() and validate_with_initial(buyable_formset):
			event = event_form.save(commit=False)
			location = location_form.save(commit=False)
			location.creator = organiser
			location.save()
			event.location = location
			event.creator = organiser
			event.save()
			for buyable_form in buyable_formset:
				if buyable_form.has_changed():
					buyable = buyable_form.save(commit=False)
					buyable.creator = organiser
					buyable.belonging_event = event
					buyable.save()
			if Event.objects.filter(creator = organiser).count() == 1:
				send_email_firstEvent(organiser)

			return redirect('events:event_organiser_list', organiser=organiser)
	else:
		event_form = EventForm()
		location_form = EventlocationForm()
		buyable_formset = BuyableModelFormSet(queryset=Buyable.objects.none(), initial = initial_data)

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser_user': organiser,
	}
	return render(request, "event/event_create.html", context)

@login_required(login_url='accounts:login')
def event_update_view(request, id):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	event = get_object_or_404(Event, id=id)
	location = event.location
	if organiser.organisation_type == 'gemeinnützig':
		initial_data = [{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},
						{'tax_rate': Buyable.ZERO},]
	else:
		initial_data = [{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},
						{'tax_rate': Buyable.NINETEEN},]
	print(organiser)
	if request.method == 'POST':
		event_form = EventForm(request.POST, instance = event)
		location_form = EventlocationForm(request.POST, instance = location)
		buyable_formset = BuyableInlineFormSet(request.POST, instance = event, initial = initial_data)
		if event_form.is_valid() and location_form.is_valid() and buyable_formset.is_valid():
			location.save()
			event.save()
			buyables = buyable_formset.save(commit=False)
			for buyable in buyables:
				buyable.creator = organiser
				buyable.save()
			for obj in buyable_formset.deleted_objects:
				obj.delete()

			return redirect('events:event_organiser_list', organiser=organiser)
	else:
		event_form = EventForm(instance = event)
		location_form = EventlocationForm(instance = location)
		buyable_formset = BuyableInlineFormSet(instance=event, initial = initial_data)

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser_user': organiser,
	}
	return render(request, "event/event_update.html", context)

def event_delete_view(request, id):
	event = get_object_or_404(Event, id=id)
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	if request.method == "POST":
		event.delete()
		return redirect('events:event_organiser_list', organiser.organisation_name)
	context = {
		"event": event,
		'organiser_user': organiser,
	}
	return render(request, "event/event_delete.html", context)

def event_organiser_list_view(request, organiser):
	o_object = get_object_or_404(Organiser, organisation_name = organiser)
	event_list = Event.objects.filter(creator = o_object)
	event_list = event_list.order_by('date')
	user = request.user
	try:
		organiser_user = Organiser.objects.get(username = request.user.username)
	except:
		organiser_user = None
	print(user)
	#print(o_object.user_adress_contact_set)
	logged_in = user.username == o_object.username
	context = {
		'request': request,
		'organiser': o_object,
		'event_list': event_list,
		'logged_in': logged_in,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
		'organiser_user': organiser_user,
	}

	if(logged_in):
		return render(request, "event/profile_organiser.html", context)
	else:
		return render(request, "event/profile_customer.html", context)


def invoiceUID_generator(size = 7, chars= string.digits):
    return 'ST'+''.join(random.choice(chars) for _ in range(size))


def send_email_firstEvent(organiser):
	subject = 'Glückwunsch! Sie haben Ihre erste Veranstaltung erstellt'
	html_message = render_to_string('event/mail_firstEvent.html')
	plain_message = strip_tags(html_message)
	if settings.DEBUG:
		to = ['roessler.paul@web.de', 'kolzmertz@gmail.com', organiser.email]
	else:
		to = [organiser.email]
	send_mail(subject, plain_message, settings.EMAIL_HOST_USER, to, html_message = html_message)

