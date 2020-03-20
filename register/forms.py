from django import forms
from .models import User
from .models import Organiser

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class DetailForm(forms.ModelForm):
    class Meta:
        model = Organiser
        fields = '__all__'
