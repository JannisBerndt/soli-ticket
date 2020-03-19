from django.db import models

class User(models.Model):
    mail = models.TextField()
    pwd = models.TextField()
    pwd_repeat = models.TextField()

    def __str__(self):
        return self.mail
