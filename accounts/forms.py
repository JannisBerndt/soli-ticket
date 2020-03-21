from django import forms
from accounts.models import Organiser

class accountsForm(forms.ModelForm):

    class Meta:
        model = Organiser
        fields = '__all__'
