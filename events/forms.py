from django import forms
from django.forms import formset_factory

from .models import Event, Eventlocation, Buyable

class EventlocationForm(forms.ModelForm):
	location_name = forms.CharField(label='Veranstaltungsort')
	city = forms.CharField(label='Stadt', required=False)
	street = forms.CharField(label='Straße', required=False)
	house_number = forms.CharField(label='Hausnummer', required=False)
	post_code = forms.DecimalField(label='Postleitzahl', required=False)
	class Meta:
		model = Eventlocation
		fields = [
			'location_name',
			'city',
			'street',
			'house_number',
			'post_code',
		]

class BuyableForm(forms.ModelForm):
	buyable_name = forms.CharField(label='Produktname', required=False)
	price = forms.DecimalField(label='Preis', required=False)
	class Meta:
		model = Buyable
		fields = [
			'buyable_name',
			'price',
		]

BuyableFormSet = formset_factory(BuyableForm, extra=1)

class EventForm(forms.ModelForm):
	# address = AddressForm()
	# buyables = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset = Buyable.objects.all().values_list('name'))
	name = forms.CharField(label='Eventname')
	description = forms.CharField(label='Beschreibung', widget=forms.Textarea)
	date = forms.DateTimeField(label='Veranstaltungsdatum', help_text='Format: DD.MM.YYYY HH:MM:SS (Uhrzeit kann auch weggelassen werden)')
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'date',
			# 'address',
			# 'buyables',
		]