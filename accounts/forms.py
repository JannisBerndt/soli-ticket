from django import forms
from accounts.models import Organiser, Order, UserAddress
from django.forms import inlineformset_factory
from events.models import Buyable


class OrderForm(forms.ModelForm):
	# article = forms.CharField(disabled=True)
	amount = forms.IntegerField(label='Anzahl', min_value=0, initial=0, widget=forms.NumberInput(attrs={'class': 'text-field-2 w-input amount-field', 'id': 'field-3', 'oninput': 'calcSum()'}))
	class Meta:
		model = Order
		fields = [
			'amount',
			# 'price',
		]



class Register1(forms.ModelForm):
	email =		forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text-field-2 w-input', 'id': 'email'}))
	user =      forms.CharField( widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'user'}))
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
	oname =   forms.CharField(label='Name der Organisation', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-der-Organisation'}))		
	description = 	forms.CharField(required=False, label='Informationen über Sie', widget=forms.Textarea(attrs={'rows': 2,'class': 'textarea-2 w-input', 'id': 'field', 'placeholder': '(optional)'}))
	CHOICES = (('gemeinnützig' , 'gemeinnützig'),('nicht gemeinnützig', 'nicht gemeinnützig'))
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
	paypal_email =	forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text-field-2 w-input', 'id': 'email', 'placeholder' : 'Email-Adresse'}))

	class Meta:
		model = Organiser
		fields = [
			'paypal_email',
		]


class OrganiserForm(forms.ModelForm):
	organisation_name = forms.CharField(label='Name der Organisation', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Name-der-Organisation'}))
	organisation_type = forms.ChoiceField(required=False, label='Art der Organisation', widget=forms.Select(attrs={'class': 'select-field w-select', 'id': 'Art'}), choices = [('gemeinnützig', 'gemeinnützig')])
	contact_first_name = forms.CharField(label='Vorname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'vorname', 'placeholder': 'Vorname'}))
	contact_last_name = forms.CharField(label='Nachname', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'nachname', 'placeholder': 'Nachname'}))
	contact_phone = forms.CharField(required=False, label='Telefonnummer', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Telenummer', 'placeholder': '(optional)'}))
	email = forms.EmailField(label='Telefonnummer', widget=forms.EmailInput(attrs={'class': 'text-field-2 w-input', 'id': 'Telenummer'}))
	iban = forms.CharField(label='IBAN', widget=forms.TextInput(attrs={'class': 'text-field-2 text-field-ind w-input', 'id': 'IBAN', 'placeholder': 'IBAN'}))
	bic = forms.CharField(label='BIC', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'BIC', 'placeholder': 'BIC'}))
	bank_account_owner = forms.CharField(label='Kontoinhaber', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Kontoinhaber', 'placeholder': 'Kontoinhaber'}))
	kontosite = forms.CharField(required=False, label='Seite der Kontodaten', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'KontoVerifikationsLink', 'placeholder': '(optional)'}))
	description = forms.CharField(required=False, label='Informationen über Sie', widget=forms.Textarea(attrs={'rows': 2,'class': 'textarea-2 w-input', 'id': 'field', 'placeholder': '(optional)'}))
	class Meta:
		model = Organiser
		fields = [
			'organisation_name',
			'organisation_type',
			'contact_first_name',
			'contact_last_name',
			'contact_phone',
			'email',
			'iban',
			'bic',
			'bank_account_owner',
			'kontosite',
			'description',
		]

class UserAddressForm(forms.ModelForm):
	strasse = forms.CharField(label='Straße', widget=forms.TextInput(attrs={'class': 'text-field-2 text-field-ind w-input', 'id': 'Stra-e', 'placeholder': 'Straße'}))
	hnummer = forms.CharField(label='Hausnummer', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'HN', 'placeholder': 'HausNr'}))
	plz = forms.CharField(label='Postleitzahl', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'PLZ', 'placeholder': 'Postleitzahl'}))
	ort = forms.CharField(label='Ort', widget=forms.TextInput(attrs={'class': 'text-field-2 w-input', 'id': 'Ort', 'placeholder': 'Ort'}))
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