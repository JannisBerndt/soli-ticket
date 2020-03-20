from django import forms

from .models import Event, Address, Buyable

class AddressForm(forms.ModelForm):
	# country = forms.CharField(required=False)
	# city = forms.CharField(required=False)
	# street = forms.CharField(required=False)
	# house_number = forms.CharField(required=False)
	# post_code = forms.DecimalField(required=False)
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
	class Meta:
		model = Buyable
		fields = [
			'name',
			'price',
		]

class EventForm(forms.ModelForm):
	address = AddressForm()
	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'date',
			# 'address',
			# 'buyables',
		]