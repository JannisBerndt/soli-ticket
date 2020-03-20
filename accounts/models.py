from django.db import models

class Account(models.Model):
    mail = models.CharField(max_length=120, null=True)
    password = models.CharField(max_length=120, null=True)
    repeat_password = models.CharField(max_length=120, null=True)

    class Meta:
        abstract = True

class Organiser(Account):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    first_name_contact = models.CharField(max_length=120)
    last_name_contact = models.CharField(max_length=120)
    phone_contact = models.CharField(max_length=120)
    iban = models.CharField(max_length=120)
    bic = models.CharField(max_length=120)
    bank_account_owner = models.CharField(max_length=120)
    website = models.CharField(max_length=120)
    shop = models.CharField(max_length=120)

    def __str__(self):
        return self.name
