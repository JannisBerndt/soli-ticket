from django import forms
from django.forms import formset_factory

from .models import Event, Address, Buyable

class AddressForm(forms.ModelForm):
	country = forms.CharField(label='Land')
	city = forms.CharField(label='Stadt')
	street = forms.CharField(label='Straße')
	house_number = forms.CharField(label='Hausnummer')
	post_code = forms.DecimalField(label='Postleitzahl')
	class Meta:
		model = Address
		fields = [
			'country',
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