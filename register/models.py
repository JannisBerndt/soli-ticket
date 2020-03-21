from django.db import models
from django.contrib.auth.models import User

class UserAddress(models.Model):
    
    strasse = models.CharField(max_length=120, null=True)
    hnummer = models.CharField(max_length=120, null=True)
    plz= models.CharField(max_length=120, null=True)
    ort = models.CharField(max_length=120, null=True)
    state = models.CharField(max_length= 40, null = True , default = None)
    country = models.CharField(max_length= 40, null = True , default = "Deutschland")

    class Meta:
        verbose_name='User_Address'
        verbose_name_plural='User_Address'

class Organiser(User):
    user_address = models.OneToOneField(
        UserAddress,
        on_delete=models.CASCADE,
        null = True
    )
    organisation_name = models.CharField(max_length=120)
    organisation_type = models.CharField(max_length=120)
    contact_first_name = models.CharField(max_length=120)
    contact_last_name = models.CharField(max_length=120)
    contact_phone = models.IntegerField(null=True)
    iban = models.CharField(max_length=120, null=True)
    bic = models.CharField(max_length=120, null=True)
    bank_account_owner = models.CharField(max_length=120, null=True)
    website = models.CharField(max_length=120, null=True)
    shop = models.CharField(max_length=120, null=True)
    
    def __str__(self):
        return self.organisation_name

    class Meta:
        verbose_name='Veranstalter'
        verbose_name_plural='Veranstalter'
