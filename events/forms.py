from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

from .models import Event, Eventlocation, Buyable

class EventlocationForm(forms.ModelForm):
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
		if data is not None:
			data = data.capitalize()
		return data

class BuyableForm(forms.ModelForm):
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
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'date',
		]
