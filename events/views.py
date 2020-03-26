from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from accounts.models import Organiser, Customer, Order
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Eventlocation, Buyable
from .forms import EventForm, EventlocationForm, BuyableForm, BuyableFormSet
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

# def event_list_view(request):
# 	queryset = Event.objects.all()
# 	context = {
# 		"event_list": queryset,
# 		'user': request.user,
# 		'authenticated': request.user.is_authenticated,
# 	}
# 	return render(request, "event/event_list.html", context)

@login_required(login_url='accounts:login')
def event_create_view(request):
	user = request.user
	organiser = get_object_or_404(Organiser, username=user.username)
	print(organiser)
	if request.method == 'POST':
		event_form = EventForm(request.POST)
		location_form = EventlocationForm(request.POST)
		buyable_formset = BuyableFormSet(request.POST)
		print(event_form)
		if event_form.is_valid() and location_form.is_valid():
			event = event_form.save(commit=False)
			location = location_form.save(commit=False)
			location.creator = organiser
			location.save()
			event.location = location
			event.creator = organiser
			event.save()
			for buyable_form in buyable_formset:
				print(buyable_form)
				buyable_form.is_valid()
				data = buyable_form.cleaned_data
				try:
					valid = (data['buyable_name'] != '') and (data['price'] != 0)
					if valid:
						print('In If')
						print(buyable_form.cleaned_data)
						buyable = buyable_form.save(commit=False)
						buyable.creator = organiser
						buyable.belonging_event = event
						buyable.save()
				except KeyError:
					pass
			return redirect('events:event_organiser_list', organiser=organiser)
	else:
		event_form = EventForm()
		location_form = EventlocationForm()
		buyable_formset = BuyableFormSet()

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

def event_update_view(request, id):
	event = get_object_or_404(Event, id=id)
	if not event.location == None:
		location = get_object_or_404(Eventlocation, id=event.location.id)
	else:
		location = None
	event_form = EventForm(request.POST or None, instance = event)
	location_form = EventlocationForm(request.POST or None, instance = location)
	if event_form.is_valid():
		event = event_form.save(commit=False)
		if location_form.is_valid():
			location = location_form.save(commit=False)
			location.creator = Organiser.objects.get(username='gfbds')
			location.save()
			event.location = location
		event.creator = Organiser.objects.get(username='gfbds')
		event.save()
		return redirect('../')

	context = {
		'event_form': event_form,
		'location_form': location_form,
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

def buyable_create_view(request, id):
	buyable_form = BuyableForm(request.POST or None)
	tip = ''
	if buyable_form.is_valid():
		data = buyable_form.cleaned_data
		if not data['buyable_name'] == '':
			buyable = buyable_form.save(commit=False)
			buyable.creator = Organiser.objects.get(username='gfbds') #needs change
			buyable.save()
			Event.objects.get(id=id).buyables.add(buyable)
			buyable_form = BuyableForm()
			return redirect('../../')
		else:
			tip = 'Bitte geben sie mindestens einen Namen an oder gehen Sie zurück'

	context = {
		'buyable_form': buyable_form,
		'tip': tip,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
	}
	return render(request, "buyable/buyable_create.html", context)

def buyable_update_view(request, id_b, id_e):
	buyable = get_object_or_404(Buyable, id=id_b)
	event = get_object_or_404(Event, id=id_e)
	buyable_form = BuyableForm(request.POST or None, instance = buyable)
	tip = ''
	if buyable_form.is_valid():
		data = buyable_form.cleaned_data
		if not data['buyable_name'] == '':
			buyable = buyable_form.save()
			event.buyables.add(buyable)
			return redirect('../../../')
		else:
			tip = 'Bitte geben sie mindestens einen Namen an oder gehen Sie zurück'

	context = {
		'buyable_form': buyable_form,
		'tip': tip,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
	}
	return render(request, "buyable/buyable_update.html", context)

def buyable_delete_view(request, id_b, id_e):
	buyable = get_object_or_404(Buyable, id=id_b)
	event = get_object_or_404(Event, id=id_e)
	if request.method == "POST":
		event.buyables.remove(buyable)
		buyable.delete()
		return redirect('../../../')
	context = {
		"buyable": buyable,
		'authenticated': request.user.is_authenticated,
	}
	return render(request, "buyable/buyable_delete.html", context)

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

# def event_create_view(request):
# 	event_form = EventForm(request.POST or None)
# 	address_form = AddressForm(request.POST or None)
# 	buyable_form = BuyableForm(request.POST or None)
# 	if event_form.is_valid():
# 		event = event_form.save(commit=False)
# 		if address_form.is_valid():
# 			address = address_form.save(commit=False)
# 			address.creator = Organiser.objects.get(username='gfbds')
# 			address.save()
# 			event.address = address
# 		event.creator = Organiser.objects.get(username='gfbds')
# 		event.save()
# 		if buyable_form.is_valid():
# 			data = buyable_form.cleaned_data
# 			print(data)
# 			if not data['buyable_name'] == '':
# 				buyable = buyable_form.save(commit=False)
# 				buyable.creator = Organiser.objects.get(username='gfbds')
# 				buyable.save()
# 				event.buyables.add(buyable)
# 		event_form = EventForm()
# 		address_form = AddressForm()
# 		buyable_form = BuyableForm()

# 	context = {
# 		'event_form': event_form,
# 		'address_form': address_form,
# 		'buyable_form': buyable_form,
# 	}
# 	return render(request, "event/event_create.html", context)

# def event_create_view(request):
# 	BuyableFormSet = formset_factory(BuyableForm, extra=2)
# 	event_form = EventForm(request.POST or None)
# 	address_form = AddressForm(request.POST or None)
# 	buyable_formset = BuyableFormSet(request.POST or None)

	# buyables = Buyable.objects.all().values_list('name', 'price')
	# 	if buyable_formset.is_valid():
	# 		for buyable_form in buyable_formset:
	# 			buyable = buyable_form.save()

# 	if event_form.is_valid():
# 		event = event_form.save(commit=False)
# 		if address_form.is_valid():
# 			address = address_form.save()
# 			event.address = address
# 		event.save()
# 		if buyable_formset.is_valid():
# 			for buyable_form in buyable_formset:
# 				buyable = buyable_form.save()
# 				event.buyables.add(buyable)

# 	context = {
# 		'event_form': event_form,
# 		'address_form': address_form,
# 		'buyable_formset': buyable_formset,
# 	}
# 	return render(request, "event/event_create.html", context)

# def event_update_view(request, id):
# 	event = get_object_or_404(Event, id=id)
# 	if not event.address == None:
# 		address = get_object_or_404(Address, id=event.address.id)
# 	else:
# 		address = None
# 	buyables = event.buyables.all()
# 	event_form = EventForm(request.POST or None, instance = event)
# 	address_form = AddressForm(request.POST or None, instance = address)
# 	BuyableFormSet = formset_factory(BuyableForm, extra=0)
# 	print(buyables.values())
# 	buyable_formset = BuyableFormSet(request.POST or None, initial=buyables.values())
# 	if event_form.is_valid():
# 		event = event_form.save(commit=False)
# 		if address_form.is_valid():
# 			address = address_form.save()
# 			event.address = address
# 		event.save()

# 		for buyable_form in buyable_formset:
# 			buyable_form.save()

# 	context = {
# 		'event_form': event_form,
# 		'address_form': address_form,
# 		'buyable_formset': buyable_formset,
# 	}
# 	return render(request, "event/event_update.html", context)

def location_create_view(request):
	location_form = EventlocationForm(request.POST or None)

	if location_form.is_valid():
		location_form.save()
		location_form = EventlocationForm()

	context = {
		'location_form': location_form,
		'user': request.user,
		'authenticated': request.user.is_authenticated,
	}
	return render(request, "location/location_create.html", context)
