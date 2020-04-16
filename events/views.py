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
from accounts.forms import OrderForm, OrderContactForm, OrderFormSet
import uuid
import random
import string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pdb

def event_detail_view(request, id, organisation_name):
	event = get_object_or_404(Event, id=id)
	organisation = event.creator
	buyables = Buyable.objects.filter(belonging_event=event)
	order_formset = OrderFormSet()
	contact_form = OrderContactForm()

	if request.method == 'POST':
		order_formset = OrderFormSet(request.POST)
		contact_form = OrderContactForm(request.POST)

		if not organisation.paypal_email:
			return render(request, 'event/error.html')

		if order_formset.is_valid() and contact_form.is_valid():
			sum = 0
			o_uid = invoiceUID_generator()
	
			for order_form in order_formset.orders_to_be_saved():
				order = order_form.save(commit=False)
				order.article = buyables[int(order_form.prefix[-1])]
				order.price = buyables[int(order_form.prefix[-1])].price * order.amount
				order.customer_mail = contact_form.cleaned_data["email"]
				order.acceptedTac = contact_form.cleaned_data["acceptedTac"]
				order.invoiceUID = o_uid
				order.save()
				sum += order.price

			if organisation.paypal_email:
				request.session["invoiceUID"] = o_uid
				request.session["sum"] = float(sum)
				request.session["paypal_email"] = organisation.paypal_email
				return redirect(reverse('accounts:events:payment:process', kwargs={'organisation_name': organisation.organisation_name, 'id': id}))

	withoutMwst = True
	for buyable in buyables:
		if buyable.tax_rate != 0.00:
			withoutMwst = False

	context = {
		'event': event,
		'buyables': buyables,
		'order_formset': order_formset,
		'formset': zip(buyables, order_formset),
		'organiser': organisation,
		'contact_form': contact_form,
		'withoutMwst': withoutMwst,
	}
	return render(request, "event/event_detail.html", context)


@login_required(login_url='accounts:login')
def event_create_view(request, organisation_name):
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
def event_update_view(request, id, organisation_name):
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

			return redirect('accounts:profile', organiser=organiser)
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

def event_delete_view(request, id, organisation_name):
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
	uid = 'ST'+''.join(random.choice(chars) for _ in range(size))
	existingUIDs = Order.objects.filter(invoiceUID = uid).values('invoiceUID')

	# Sollten schon Orders dazu existieren, wird solange eine neue UID erzeugt und die Daten geholt, bis des Queryset o_orders leer ist.
	while existingUIDs:
		uid = 'ST'+''.join(random.choice(chars) for _ in range(size))
		existingUIDs = Order.objects.filter(invoiceUID = uid).values('invoiceUID')
	return uid


def send_email_firstEvent(organiser):
	subject = 'Glückwunsch! Sie haben Ihre erste Veranstaltung erstellt'
	html_message = render_to_string('email/first_event_created.html')
	plain_message = strip_tags(html_message)
	if settings.DEBUG:
		to = ['roessler.paul@web.de', 'kolzmertz@gmail.com', organiser.email]
	else:
		to = [organiser.email]
	send_mail(subject, plain_message, settings.EMAIL_HOST_USER, to, html_message = html_message)
