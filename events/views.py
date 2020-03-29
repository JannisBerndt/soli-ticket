from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from accounts.models import Organiser, Customer, Order
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from .models import Event, Eventlocation, Buyable
from .forms import EventForm, EventlocationForm, BuyableForm, BuyableFormSet, BuyableInlineFormSet, BuyableModelFormSet
from accounts.forms import OrderForm

def event_detail_view(request, id):
	event = get_object_or_404(Event, id=id)
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
		if order_formset.is_valid():
			i=0
			sum = 0
			orders = []
			for order_form in order_formset:
				order = order_form.save(commit=False)
				if order.amount:
					order.article = buyables[i]
					order.price = buyables[i].price * order.amount
					order.customer = customer
					order.customer_mail = request.POST.get('field-4')
					order.save()
					sum += order.price
					orders.append(order)
				i += 1

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

				subject = 'Ihre Spende auf www.Soli-Ticket.de'
				message = 'Hallo! \n\n\
Vielen Dank, dass Sie Ihre Spende in Höhe von ' + str(sum) + '€ zugesagt haben. ' + organiser.organisation_name + ' bedankt sich vielmals dafür! \n\
Sie leisten mit Ihrer Spende einen wichtigen Beitrag dazu, kritische Einnahmeausfälle abzumildern und unsere Kulturlandschaft zu erhalten. Vielen, vielen Dank! \n\
Hier nochmal Ihre Spendedaten zur Übersicht. Bitte überweisen Sie (falls noch nicht geschehen) noch heute - damit ' + organiser.organisation_name + ' \
direkt von Ihrer Spende profitiert: \n\n\
Gesamtbetrag: ' + str(sum) + '€ \n\
Kontoinhaber: ' + organiser.bank_account_owner + ' \n\
IBAN: ' + organiser.iban +  '\n\
BIC: ' + organiser.bic + ' \n\
Verwendungszweck: Spende über Soli-Ticket \n\n\
Viele Grüße und vielen, vielen Dank von ' + organiser.organisation_name + ' und dem Team von www.soli-ticket.de ! \n\n\
P.S. Sie wollen kostenfrei noch mehr beitragen? Teilen Sie www.soli-ticket.de und alle interessanten Veranstaltungen mit Ihren Kontakten!'

				#print(message)

				send_mail(subject, message, settings.EMAIL_HOST_USER, [request.POST.get('field-4')])

				return render(request, "event/event_donate.html", context)

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
	print(organiser)
	if request.method == 'POST':
		event_form = EventForm(request.POST)
		location_form = EventlocationForm(request.POST)
		buyable_formset = BuyableModelFormSet(request.POST, queryset=Buyable.objects.none())
		if event_form.is_valid() and location_form.is_valid() and buyable_formset.is_valid():
			event = event_form.save(commit=False)
			location = location_form.save(commit=False)
			location.creator = organiser
			location.save()
			event.location = location
			event.creator = organiser
			event.save()
			buyables = buyable_formset.save(commit=False)
			for buyable in buyables:
				buyable.creator = organiser
				buyable.belonging_event = event
				buyable.save()
			return redirect('events:event_organiser_list', organiser=organiser)
	else:
		event_form = EventForm()
		location_form = EventlocationForm()
		buyable_formset = BuyableModelFormSet(queryset=Buyable.objects.none())

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser': organiser,
		'organiser_user': organiser,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
	}
	return render(request, "event/event_create.html", context)

@login_required(login_url='accounts:login')
def event_update_view(request, id):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	event = get_object_or_404(Event, id=id)
	location = event.location
	print(organiser)
	if request.method == 'POST':
		event_form = EventForm(request.POST, instance = event)
		location_form = EventlocationForm(request.POST, instance = location)
		buyable_formset = BuyableInlineFormSet(request.POST, instance = event)
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
		buyable_formset = BuyableInlineFormSet(instance=event)

	context = {
		'event_form': event_form,
		'location_form': location_form,
		'buyable_formset': buyable_formset,
		'organiser': organiser,
		'organiser_user': organiser,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
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
		'organiser': organiser,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
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

	return render(request, "event/event_list_organiser.html", context)
	