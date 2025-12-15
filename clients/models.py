from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    join_date = models.DateField()
    expiry_date = models.DateField()
    membership_days = models.IntegerField()

    def __str__(self):
        return self.name