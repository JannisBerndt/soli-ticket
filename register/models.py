from django.db import models

class User(models.Model):
    mail = models.CharField(max_length=200)
    pwd = models.CharField(max_length=200)
    pwd_repeat = models.CharField(max_length=200)

    def __str__(self):
        return self.mail
