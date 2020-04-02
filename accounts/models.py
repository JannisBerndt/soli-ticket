from django.db import models
from django.contrib.auth.models import User


class UserAddress(models.Model):
    strasse = models.CharField(max_length=120, null=True)
    hnummer = models.CharField(max_length=120, null=True)
    plz= models.CharField(max_length = 40, null=True)
    ort = models.CharField(max_length=120, null=True)
    state = models.CharField(max_length= 40, null = True , default = None)
    country = models.CharField(max_length= 40, null = True , default = "Deutschland")


    class Meta:
        verbose_name='User Address'
        verbose_name_plural='User Address'


    def __str__(self):
        return self.strasse


class Organiser(User):
    user_address = models.OneToOneField(
        UserAddress,
        on_delete=models.CASCADE,
        null = True,
        related_name = "user_adress_contact_set",
        related_query_name="organiser_address"
    )
    organisation_name = models.CharField(max_length=120)
    organisation_type = models.CharField(max_length=120)
    contact_first_name = models.CharField(max_length=120)
    contact_last_name = models.CharField(max_length=120)
    contact_phone = models.CharField(null=True, max_length=100)
    iban = models.CharField(max_length=120, null=True)
    bic = models.CharField(max_length=120, null=True)
    bank_account_owner = models.CharField(max_length=120, null=True)
    kontosite = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    paypal_email = models.EmailField(null=True,max_length=254)


    def __str__(self):
        return self.organisation_name


    class Meta:
        verbose_name='Organiser'
        verbose_name_plural='Organiser'


class Customer(User):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name='Customer'
        verbose_name_plural='Customers'


class Order(models.Model):
    article = models.ForeignKey('events.Buyable', null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='customer_set')
    customer_mail = models.EmailField(max_length=120, null=True)
    amount = models.PositiveIntegerField(null=True)
    price = models.DecimalField(null=True, max_digits=1000, decimal_places=2)
    createdDateTime = models.DateTimeField(auto_now_add=True)
    changedDateTime = models.DateTimeField(auto_now=True)
