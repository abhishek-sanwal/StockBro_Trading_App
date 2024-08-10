from django.db import models

# Create your models here.


class Stockdeatils(models.Model):

    symbol = models.CharField(max_length=40)
    companyName = models.TextField()
    industry = models.CharField(max_length=200)
