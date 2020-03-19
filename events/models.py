from django.db import models

# Create your models here.

class Buyable(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=1000, decimal_places=2)

class Address(models.Model):
	country = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	street = models.CharField(max_length=120)
	house_number = models.CharField(max_length=120)
	post_code = models.DecimalField(max_digits=5, decimal_places=0)

class Event(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
	# buyable = models.ManyToManyField(Buyable, null=True, blank=True)
	# from .Address import country, city, street, house_number, post_code
	
	country = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	street = models.CharField(max_length=120)
	house_number = models.CharField(max_length=120)
	post_code = models.DecimalField(max_digits=5, decimal_places=0)

