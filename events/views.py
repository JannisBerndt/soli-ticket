from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from accounts.models import Organiser, Customer, Order
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django import forms
from decimal import Decimal
from .models import Event, Eventlocation, Buyable
from .forms import EventForm, EventlocationForm, BuyableForm, BuyableFormSet, BuyableInlineFormSet, BuyableModelFormSet, validate_with_initial
from accounts.forms import OrderForm, OrderContactForm
import uuid
import random
import string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pdb

def event_detail_view(request, id, organiser):
	event = get_object_or_404(Event, id=id)
	o_organiser = Organiser.objects.get(organisation_name=event.creator.organisation_name)

	buyables = Buyable.objects.filter(belonging_event=event)
	location = event.location
	OrderFormSet = inlineformset_factory(Customer, Order, form=OrderForm, fields=['amount',], extra=buyables.count())
	order_formset = OrderFormSet(queryset=Order.objects.none())
	contact_form = OrderContactForm()

	if request.method == 'POST':
		try:
			customer = Customer.objects.get(username=request.user.username)
		except:
			customer = None

		order_formset = OrderFormSet(request.POST, instance=customer)
		contact_form = OrderContactForm(request.POST)

		o_Event = Event.objects.get(id = id)
		o_Organisation = Organiser.objects.get(id = o_Event.creator_id)

		if not o_Organisation.paypal_email:
			return render(request, 'event/error.html')

		if order_formset.is_valid() and contact_form.is_valid():
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
					order.customer_mail = contact_form.cleaned_data["email"]
					order.acceptedTac = contact_form.cleaned_data["acceptedTac"]
					order.invoiceUID = o_uid
					order.save()
					sum += order.price
					orders.append(order)
				i += 1
			sum = float(sum)
			if orders:
				o_organiser = event.creator
				context = {
					'sum': sum,
					'organiser': o_organiser,
					'orders': orders,
					'event': event,
					'authenticated': request.user.is_authenticated,
				}

				if o_organiser.paypal_email:
					request.session["invoiceUID"] = o_uid
					request.session["sum"] = sum
					request.session["paypal_email"] = o_organiser.paypal_email
					print(organiser)
					return redirect(reverse('accounts:events:payment:process', kwargs={'organiser': organiser, 'id': id}))

	withoutMwst = True
	for buyable in buyables:
		if buyable.tax_rate != 0.00:
			withoutMwst = False

	formset = zip(buyables, order_formset)
	context = {
		'event': event,
		'buyables': buyables,
		'location': location,
		'order_formset': order_formset,
		'formset': formset,
		'organiser': organiser,
		'contact_form': contact_form,
		'withoutMwst': withoutMwst,
	}
	return render(request, "event/event_detail.html", context)


@login_required(login_url='accounts:login')
def event_create_view(request, organiser):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	if request.method == 'POST':
		event_form = EventForm(request.POST)
		location_form = EventlocationForm(request.POST)
		buyable_formset = BuyableModelFormSet(request.POST, queryset=Buyable.objects.none())
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
			try:
				organiser.acceptedTac = True if request.POST.get("checkbox") != "" else False
				organiser.save()
			except:
				pass
			return redirect('accounts:profile', organiser=organiser)
	else:
		event_form = EventForm()
		location_form = EventlocationForm()
		buyable_formset = BuyableModelFormSet(queryset=Buyable.objects.none())

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser_user': organiser,
	}
	return render(request, "event/event_create.html", context)

@login_required(login_url='accounts:login')
def event_update_view(request, id, organiser):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	event = get_object_or_404(Event, id=id)
	location = event.location
	if request.method == 'POST':
		event_form = EventForm(request.POST, instance = event)
		location_form = EventlocationForm(request.POST, instance = location)
		buyable_formset = BuyableInlineFormSet(request.POST, instance = event)
		if event_form.is_valid() and location_form.is_valid() and buyable_formset.is_valid():
			location.save()
			event.save()
			buyables = buyable_formset.save(commit=False)
			print(buyables)
			for buyable in buyables:
				buyable.creator = organiser
				buyable.save()
			for obj in buyable_formset.deleted_objects:
				obj.delete()

			return redirect('accounts:profile', organisation_name=organiser.organisation_name)
	else:
		event_form = EventForm(instance = event)
		location_form = EventlocationForm(instance = location)
		buyable_formset = BuyableInlineFormSet(instance=event)

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser_user': organiser,
	}
	return render(request, "event/event_update.html", context)

def event_delete_view(request, id, organiser):
	event = get_object_or_404(Event, id=id)
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	if request.method == "POST":
		event.delete()
		return redirect('accounts:profile', organiser.organisation_name)
	context = {
		"event": event,
		'organiser_user': organiser,
	}
	return render(request, "event/event_delete.html", context)


def profile_redirect_view(request, organiser):
	return redirect('accounts:profile', organiser)

def event_detail_redirect_view(request, id):
	event = get_object_or_404(Event, id=id)
	return redirect('accounts:events:event_detail', id=id, organiser=event.creator.organisation_name)


def invoiceUID_generator(size = 7, chars= string.digits):
    return 'ST'+''.join(random.choice(chars) for _ in range(size))


def send_email_firstEvent(organiser):
	subject = 'Glückwunsch! Sie haben Ihre erste Veranstaltung erstellt'
	html_message = render_to_string('email/first_event_created.html')
	plain_message = strip_tags(html_message)
	if settings.DEBUG:
		to = ['roessler.paul@web.de', 'kolzmertz@gmail.com', organiser.email]
	else:
		to = [organiser.email]
	send_mail(subject, plain_message, settings.EMAIL_HOST_USER, to, html_message = html_message)
