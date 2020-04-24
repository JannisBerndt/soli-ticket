from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from solisite.settings import HOST_URL_BASE

class UserAddress(models.Model):
    strasse = models.CharField(max_length=120)
    hnummer = models.CharField(max_length=120)
    plz = models.CharField(max_length=40)
    ort = models.CharField(max_length=120)
    country = models.CharField(max_length= 40, default = "Deutschland")

    class Meta:
        verbose_name='User Address'
        verbose_name_plural='User Address'

    def __str__(self):
        return self.strasse

    def getWholeAddress(self):
        return self.strasse + " " + self.hnummer + ", " + self.plz + " " + self.ort


class Organiser(User):
    TYPES = (
        ('gemeinnützig', 'gemeinnützig'),
        ('nicht gemeinnützig', 'nicht gemeinnützig'),
    )
    user_address = models.OneToOneField(
        UserAddress,
        on_delete=models.CASCADE,
        null = True,
        related_name = "user_adress_contact_set",
        related_query_name="organiser_address"
    )
    organisation_name = models.CharField(max_length=120)
    organisation_type = models.CharField(max_length=120, choices=TYPES)
    contact_first_name = models.CharField(max_length=120)
    contact_last_name = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=100, null=True, blank=True)
    iban = models.CharField(max_length=120, null=True, blank=True)
    bic = models.CharField(max_length=120, null=True, blank=True)
    bank_account_owner = models.CharField(max_length=120, null=True, blank=True)
    kontosite = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    paypal_email = models.EmailField(null=True, blank=True, max_length=254)
    isActivated = models.BooleanField(default = True)
    confirmationCode = models.CharField(max_length = 60, default = 'nicht_migrierte_daten')
    acceptedTac = models.BooleanField() # The Organiser has accepted our terms and conditions

    picture = models.ImageField(null=True, blank=True, default = "default.png")

    def __str__(self):
        return self.organisation_name

    def get_share_url(self):
        return "{}{}".format(HOST_URL_BASE, reverse("accounts:profile", kwargs={"organisation_name": self.organisation_name})[1:])

    def get_confirm_url(self):
        return "{}{}?confirmationCode={}&id={}".format(HOST_URL_BASE, reverse("accounts:confirm")[1:], self.confirmationCode, self.id)

    def getContactPerson(self):
        return self.contact_first_name + " " + self.contact_last_name

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
    article = models.ForeignKey('events.Buyable', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='customer_set')
    customer_mail = models.EmailField(max_length=120)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    price = models.DecimalField(max_digits=1000, decimal_places=2, validators=[MinValueValidator(0)])
    createdDateTime = models.DateTimeField(auto_now_add=True)
    changedDateTime = models.DateTimeField(auto_now=True)
    invoiceUID = models.CharField(max_length = 64, default = 'nicht_migrierte_orders')
    isPayed = models.BooleanField(default = False)
    acceptedTac = models.BooleanField()

    def setPrice(self):
        self.price = self.article.price * self.amount
