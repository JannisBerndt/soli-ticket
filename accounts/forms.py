from django import forms
from accounts.models import Organiser, Order
from django.forms import formset_factory

class OrderForm(forms.ModelForm):
	article = forms.CharField(widget=forms.TextInput())
	amount = forms.IntegerField(label='Anzahl', min_value=0, initial=0, widget=forms.NumberInput(attrs={'class': 'text-field-2 w-input', 'id': 'field-3'}))
	class Meta:
		model = Order
		fields = [
			'article',
			'amount',
		]

OrderFormSet = formset_factory(OrderForm, extra=0)