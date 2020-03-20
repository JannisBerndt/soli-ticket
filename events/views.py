from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory

from .models import Event, Address
from .forms import EventForm, AddressForm, BuyableForm
# Create your views here.

def event_detail_view(request, id):
	obj = get_object_or_404(Event, id=id)
	buyables = obj.buyables.all()
	context = {
		"object": obj,
		"buyables": buyables,
		'address': obj.address,
	}
	return render(request, "event/event_detail.html", context)

def event_list_view(request):
	queryset = Event.objects.all()
	context = {
		"object_list": queryset,
	}
	return render(request, "event/event_list.html", context)

def event_create_view(request):
	BuyableFormSet = formset_factory(BuyableForm, extra=2)
	event_form = EventForm(request.POST or None)
	address_form = AddressForm(request.POST or None)
	buyable_formset = BuyableFormSet(request.POST or None)

	if event_form.is_valid():
		event = event_form.save(commit=False)
		if address_form.is_valid():
			address = address_form.save()
			event.address = address
		event.save()
		if buyable_formset.is_valid():
			for buyable_form in buyable_formset:
				buyable = buyable_form.save()
				event.buyables.add(buyable)

	context = {
		'event_form': event_form,
		'address_form': address_form,
		'buyable_formset': buyable_formset,
	}
	return render(request, "event/event_create.html", context)

def event_update_view(request, id):
	event = get_object_or_404(Event, id=id)
	if not event.address == None:
		address = get_object_or_404(Address, id=event.address.id)
	else:
		address = None
	buyables = event.buyables.all()
	event_form = EventForm(request.POST or None, instance = event)
	address_form = AddressForm(request.POST or None, instance = address)
	BuyableFormSet = formset_factory(BuyableForm, extra=0)
	print(buyables.values())
	buyable_formset = BuyableFormSet(request.POST or None, initial=buyables.values())
	if event_form.is_valid():
		event = event_form.save(commit=False)
		if address_form.is_valid():
			address = address_form.save()
			event.address = address
		event.save()
		
		# for buyable_form in buyable_formset:
		# 	buyable_form.save()

	context = {
		'event_form': event_form,
		'address_form': address_form,
		'buyable_formset': buyable_formset,
	}
	return render(request, "event/event_update.html", context)

def address_create_view(request):
	address_form = AddressForm(request.POST or None)

	if address_form.is_valid():
		address_form.save()
		address_form = AddressForm()

	context = {
		'address_form': address_form,
	}
	return render(request, "address/address_create.html", context)