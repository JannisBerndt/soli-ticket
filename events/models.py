from django.db import models
from django.urls import reverse
from accounts.models import Organiser

class Buyable(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE)
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	buyable_name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)

class Eventlocation(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE)
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	location_name = models.CharField(max_length=120)
	country = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120, null=True, blank=True)
	street = models.CharField(max_length=120, null=True, blank=True)
	house_number = models.CharField(max_length=120, null=True, blank=True)
	post_code = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)

class Event(models.Model):
	creator = models.ForeignKey(Organiser, on_delete=models.CASCADE)
	createdDateTime = models.DateTimeField(auto_now_add=True)
	changedDateTime = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	location = models.ForeignKey(Eventlocation, on_delete=models.SET_NULL, null=True)
	buyables = models.ManyToManyField(Buyable, blank=True)

	def get_absolute_url(self):
		return reverse("events:event_detail", kwargs={"id": self.id})
