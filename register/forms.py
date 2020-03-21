from django import forms
from .models import Organiser

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Organiser
        fields = '__all__'
