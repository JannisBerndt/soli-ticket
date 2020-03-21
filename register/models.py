from django.db import models
from django.contrib.auth.models import User

class Organiser(User):
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
