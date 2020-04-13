from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def val_chars(value):
    for c in value:
        if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@.+-_'":
            raise ValidationError( _('Der Benutzername darf nur aus Buchstaben, Zahlen und @/./+/-/_ bestehen'))