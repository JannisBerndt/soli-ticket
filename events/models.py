from django.db import models
from django.urls import reverse
from accounts.models import Organiser

class Eventlocation(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "address_contact_set",
								related_query_name="event_location")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	location_name = models.CharField(max_length=120)
	country = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120, null=True, blank=True)
	street = models.CharField(max_length=120, null=True, blank=True)
	house_number = models.CharField(max_length=120, null=True, blank=True)
	post_code = models.CharField(null=True, blank=True)

	def __str__(self):
		return self.location_name

class Event(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "event_contact_set",
								related_query_name="event")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	date = models.DateField(null=True, blank=True)
	time = models.TimeField(null=True, blank=True)
	location = models.ForeignKey(Eventlocation, on_delete=models.SET_NULL, null=True, related_name='+')

	def get_absolute_url(self):
		return reverse("events:event_detail", kwargs={"id": self.id})

	def get_share_url(self):
		return reverse("events:event_organiser_list", kwargs={'organiser': self.creator.organisation_name})

	def __str__(self):
		return self.name

class Buyable(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE, 
								related_name = "buyable_contact_set",
								related_query_name="buyable")
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	buyable_name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=1000, decimal_places=2)
	belonging_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_buyable', related_query_name='buyables_set')

	def __str__(self):
		return self.buyable_name