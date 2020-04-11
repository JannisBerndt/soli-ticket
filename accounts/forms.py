from django import forms
from accounts.models import Organiser, Order, UserAddress
from django.forms import inlineformset_factory
from events.models import Buyable, Event
from .helpers.validators import *

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = [
			'amount',
		]



class Register1(forms.ModelForm):
	email =		forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text-field-2 w-input', 'id': 'email'}))
	user =      forms.CharField(widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'user'}),
				validators=[val_chars], strip =False, max_length=30)
	pw1 = 		forms.CharField(max_length=32, widget=forms.PasswordInput(attrs = {'class' :"text-field-2 w-input"}))
	pw2 = 		forms.CharField(max_length=32, widget=forms.PasswordInput(attrs = {'class' :"text-field-2 w-input"}))
	class Meta:
		model = Organiser
		fields = [
			'email',
			'user',
			'pw1',
			'pw2',
		]
	

class Register2(forms.ModelForm):
	vname =	 forms.CharField(label='Vorname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'vorname', 'placeholder': 'Vorname'}))	
	nname =      forms.CharField(label='Nachname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'nachname', 'placeholder': 'Nachname'}))
	oname =   forms.CharField(label='Name der Organisation', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-der-Organisation', 'placeholder': 'Name der Organisation'}))		
	description = 	forms.CharField(required=False, label='Informationen über Sie', widget=forms.Textarea(attrs={'rows': 2,'class': 'textarea-2 w-input', 'id': 'field', 'placeholder': '(optional)'}))
	CHOICES = ((None, 'Bitte wählen'), ('gemeinnützig' , 'gemeinnützig'), ('nicht gemeinnützig', 'nicht gemeinnützig'))
	art =	forms.ChoiceField(choices=CHOICES, widget= forms.Select(attrs ={'class':'select-field w-select'}))
	strasse = forms.CharField(label='Straße', widget=forms.TextInput(attrs={'class': 'text-field-2 text-field-ind w-input', 'id': 'Stra-e', 'placeholder': 'Straße'}))
	hnummer = forms.CharField(label='Hausnummer', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'HN', 'placeholder': 'HausNr'}))
	plz = forms.CharField(label='Postleitzahl', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'PLZ', 'placeholder': 'Postleitzahl'}))
	ort = forms.CharField(label='Ort', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Ort', 'placeholder': 'Ort'}))
	telnr = forms.CharField(required=False, label='Telefonnummer', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Telenummer', 'placeholder': '(optional)'}))
	
	class Meta:
		model = Organiser
		fields = [
			'vname',
			'nname',
			'oname',
			'description',
			'art',
			'strasse',
			'hnummer',
			'plz',
			'ort',
			'telnr',
		]

class Register3(forms.ModelForm):
	paypal_email =	forms.EmailField(required=False,widget=forms.EmailInput(attrs={'class': 'text-field-2 w-input', 'id': 'email', 'placeholder' : 'Email-Adresse'}))
	acceptedTac = forms.BooleanField(required=True)
	class Meta:
		model = Organiser
		fields = [
			'paypal_email',
			'acceptedTac',
		]


class OrganiserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = Organiser
		fields = [
			'organisation_name',
			'organisation_type',
			'contact_first_name',
			'contact_last_name',
			'contact_phone',
			'email',
			'paypal_email',
			'description',
		]

	def clean_paypal_email(self, *args, **kwargs):
		paypal_email = self.cleaned_data["paypal_email"]
		events = Event.objects.filter(creator = Organiser.objects.get(organisation_name = self.cleaned_data["organisation_name"]))
		if paypal_email:
			return paypal_email
		else:
			if events:
				raise forms.ValidationError("Da Sie bereits Events zu Ihrem Account hinzugefügt haben, müssen Sie eine Email Adresse zu Ihrem Paypal-Konto angeben.")
			else:
				return paypal_email


class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'strasse',
			'hnummer',
			'plz',
			'ort',
		]
	
	def clean_ort(self):
		data = self.cleaned_data["ort"]
		data = data.capitalize()
		return data