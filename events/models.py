from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from accounts.models import Organiser
from decimal import Decimal
from solisite.settings import HOST_URL_BASE

class Eventlocation(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "address_contact_set",
								related_query_name="event_location")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	location_name = models.CharField(max_length=120)
	country = models.CharField(max_length=120, null=True, blank=True, default="Deutschland")
	city = models.CharField(max_length=120, null=True, blank=True)
	street = models.CharField(max_length=120, null=True, blank=True)
	house_number = models.CharField(max_length=120, null=True, blank=True)
	post_code = models.CharField(max_length=40, null=True, blank=True)

	def __str__(self):
		return self.location_name

class Event(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "event_contact_set",
								related_query_name="event")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=120)
	description = models.TextField()
	date = models.DateField()
	time = models.TimeField(null=True, blank=True)
	location = models.ForeignKey(Eventlocation, on_delete=models.SET_NULL, null=True, related_name='+')

	def get_absolute_url(self):
		return reverse("events:event_detail", kwargs={"id": self.id})

	def get_share_url(self):
		return "{}{}".format(HOST_URL_BASE, reverse("events:event_detail", kwargs={"id": self.id})[1:])

	def __str__(self):
		return self.name

class Buyable(models.Model):
	SEVEN = round(Decimal(0.07), 2)
	NINETEEN = round(Decimal(0.19), 2)
	ZERO = round(Decimal(0.00), 2)
	TAX_RATES = [(NINETEEN, '19%'), (SEVEN, '7%'), (ZERO, '0%')]
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "buyable_contact_set",
								related_query_name="buyable")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	buyable_name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=1000, decimal_places=2, validators=[MinValueValidator(0)])
	belonging_event = models.ForeignKey(Event, on_delete=models.CASCADE,
										related_name='event_buyable',
										related_query_name='buyables_set')
	tax_rate = models.DecimalField(decimal_places = 2, max_digits = 3, choices=TAX_RATES, default = NINETEEN)

	def __str__(self):
		return self.buyable_name