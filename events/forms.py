from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

from .models import Event, Eventlocation, Buyable

class EventlocationForm(forms.ModelForm):
	location_name = forms.CharField(label='Veranstaltungsort', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-Des-Veranstaltungsortes', 'placeholder': "Name des Veranstaltungsortes"}))
	city = forms.CharField(label='Stadt', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Ort', 'placeholder': "Ort (Optional)"}))
	street = forms.CharField(label='Straße', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 text-field-ind w-input', 'id': 'Stra-e', 'placeholder': "Straße (Optional)"}))
	house_number = forms.CharField(label='Hausnummer', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'HN', 'placeholder': "HausNr (Optional)"}))
	post_code = forms.CharField(label='Postleitzahl', required=False, widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'PLZ', 'placeholder': "Postleitzahl (Optional)"}))
	class Meta:
		model = Eventlocation
		fields = [
			'location_name',
			'city',
			'street',
			'house_number',
			'post_code',
		]

	def clean_city(self):
		data = self.cleaned_data["city"]
		data = data.capitalize()
		return data

class BuyableForm(forms.ModelForm):
	buyable_name = forms.CharField(label='Produktname',  widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Bezeichnung-3', 'placeholder': 'Bezeichnung des Tickets/Getränks/der Speise'}))
	price = forms.DecimalField(label='Preis', widget=forms.NumberInput(attrs={'class': 'text-field-2 w-input', 'id': 'field-3', 'placeholder': "0,00"}), min_value=0)
	# tax_rate = forms.ChoiceField(label='Steuerrate', widget=forms.Select(attrs={'class': 'text-field-2 w-select'}), choices = Buyable.TAX_RATES)
	class Meta:
		model = Buyable
		fields = [
			'buyable_name',
			'price',
			'tax_rate',
		]
		
BuyableFormSet = formset_factory(BuyableForm, extra=5, max_num=5)
BuyableInlineFormSet = inlineformset_factory(Event, Buyable, form=BuyableForm, extra=5, max_num = 5)
BuyableModelFormSet = modelformset_factory(Buyable, form=BuyableForm, extra=5, max_num = 5)

def validate_with_initial(formset):
	valid = True
	for form in formset:
		if form.has_changed():
			if not form.is_valid():
				valid = False
				print('INVALID')
	return valid

class EventForm(forms.ModelForm):
	name = forms.CharField(label='Eventname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-Des-Veranstaltungsortes', 'placeholder': "Veranstaltungsname"}))
	description = forms.CharField(label='Beschreibung', widget=forms.Textarea(attrs={'class': 'textarea text-field-2 w-input', 'id': 'field-4', 'placeholder': 'Erzählen Sie mehr!'}))
	date = forms.DateField(label='Veranstaltungsdatum', widget=forms.DateInput(attrs={'class': 'text-field-2 w-input', 'id': 'DateTime', 'placeholder': "Format: DD.MM.YYYY"}))
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'date',
		]
