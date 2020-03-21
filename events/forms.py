from django import forms
from django.forms import formset_factory

from .models import Event, Eventlocation, Buyable

class EventlocationForm(forms.ModelForm):
	location_name = forms.CharField(label='Veranstaltungsort', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-Des-Veranstaltungsortes', 'placeholder': "Name des Veranstaltungsortes"}))
	city = forms.CharField(label='Stadt', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Ort', 'placeholder': "Ort (Optional)"}))
	street = forms.CharField(label='Straße', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 text-field-ind w-input', 'id': 'Stra-e', 'placeholder': "Straße (Optional)"}))
	house_number = forms.CharField(label='Hausnummer', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'HN', 'placeholder': "HausNr (Optional)"}))
	post_code = forms.DecimalField(label='Postleitzahl', required=False, widget=forms.NumberInput(attrs={'class': 'text-field-2 w-input', 'id': 'PLZ', 'placeholder': "Postleitzahl (Optional)"}))
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
	buyable_name = forms.CharField(label='Produktname', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Bezeichnung-3', 'placeholder': "Bezeichnung (z.B. &quot;Solidaritätsticket Kat. A&quot;)"}))
	price = forms.DecimalField(label='Preis', required=False,widget=forms.NumberInput(attrs={'class': 'text-field-2 w-input', 'id': 'field-3', 'placeholder': "0,00"}))
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
	name = forms.CharField(label='Eventname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-Des-Veranstaltungsortes', 'placeholder': "Veranstaltungsname"}))
	description = forms.CharField(label='Beschreibung', widget=forms.Textarea(attrs={'class': 'textarea text-field-2 w-input', 'id': 'field-4', 'placeholder': 'Erzählen Sie mehr!'}))
	date = forms.DateTimeField(label='Veranstaltungsdatum', widget=forms.DateTimeInput(attrs={'class': 'text-field-2 w-input', 'id': 'DateTime', 'placeholder': "Format: DD.MM.YYYY HH:MM:SS (Uhrzeit optional)"}))
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'date',
			# 'address',
			# 'buyables',
		]