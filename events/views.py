from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory

from accounts.models import Organiser
from .models import Event, Address, Buyable
from .forms import EventForm, AddressForm, BuyableForm, BuyableFormSet
# Create your views here.

def event_detail_view(request, id):
	event = get_object_or_404(Event, id=id)
	buyables = event.buyables.all()
	address = event.address
	context = {
		"event": event,
		"buyables": buyables,
		'address': address,
	}
	return render(request, "event/event_detail.html", context)

def event_list_view(request):
	queryset = Event.objects.all()
	context = {
		"event_list": queryset,
	}
	return render(request, "event/event_list.html", context)

def event_create_view(request):
	event_form = EventForm(request.POST or None)
	address_form = AddressForm(request.POST or None)
	buyable_form = BuyableForm(request.POST or None)
	if event_form.is_valid():
		event = event_form.save(commit=False)
		if address_form.is_valid():
			address = address_form.save(commit=False)
			address.creator = User.objects.get(id=1)
			address.save()
			event.address = address
		event.creator = User.objects.get(id=1)
		event.save()
		if buyable_form.is_valid():
			data = buyable_form.cleaned_data
			print(data)
			if not data['buyable_name'] == '':
				buyable = buyable_form.save(commit=False)
				buyable.creator = User.objects.get(id=1)
				buyable.save()
				event.buyables.add(buyable)
		event_form = EventForm()
		address_form = AddressForm()
		buyable_form = BuyableForm()

	context = {
		'event_form': event_form,
		'address_form': address_form,
		'buyable_form': buyable_form,
	}
	return render(request, "event/event_create.html", context)

def event_update_view(request, id):
	event = get_object_or_404(Event, id=id)
	if not event.address == None:
		address = get_object_or_404(Address, id=event.address.id)
	else:
		address = None
	event_form = EventForm(request.POST or None, instance = event)
	address_form = AddressForm(request.POST or None, instance = address)
	if event_form.is_valid():
		event = event_form.save(commit=False)
		if address_form.is_valid():
			address = address_form.save(commit=False)
			address.creator = User.objects.get(id=1)
			address.save()
			event.address = address
		event.creator = User.objects.get(id=1)
		event.save()
		return redirect('../')

	context = {
		'event_form': event_form,
		'address_form': address_form,
	}
	return render(request, "event/event_update.html", context)

def event_delete_view(request, id):
	event = get_object_or_404(Event, id=id)
	if request.method == "POST":
		event.delete()
		return redirect('../../')
	context = {
		"event": event,
	}
	return render(request, "event/event_delete.html", context)

def buyable_create_view(request, id):
	buyable_form = BuyableForm(request.POST or None)
	tip = ''
	if buyable_form.is_valid():
		data = buyable_form.cleaned_data
		if not data['buyable_name'] == '':
			buyable = buyable_form.save(commit=False)
			buyable.creator = User.objects.get(id=1) #needs change
			buyable.save()
			Event.objects.get(id=id).buyables.add(buyable)
			buyable_form = BuyableForm()
			return redirect('../../')
		else:
			tip = 'Bitte geben sie mindestens einen Namen an oder gehen Sie zurück'

	context = {
		'buyable_form': buyable_form,
		'tip': tip,
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
	}
	return render(request, "buyable/buyable_delete.html", context)

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

def address_create_view(request):
	address_form = AddressForm(request.POST or None)

	if address_form.is_valid():
		address_form.save()
		address_form = AddressForm()

	context = {
		'address_form': address_form,
	}
	return render(request, "address/address_create.html", context)
