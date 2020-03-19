from django.db import models

class User(models.Model):
    mail = models.CharField(max_length=120)
    pwd = models.CharField(max_length=120)
    pwd_repeat = models.CharField(max_length=120)
