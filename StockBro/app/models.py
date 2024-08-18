from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Stockdeatils(models.Model):

    symbol = models.CharField(
        max_length=40, unique=True, blank=False, null=False)
    companyName = models.TextField(blank=False, null=False)
    industry = models.CharField(max_length=200)
    prevClose = models.FloatField(default=0.0)
    lastPrice = models.IntegerField(default=0.0)
    percentChange = models.FloatField(default=0.0)
    lowerCircuit = models.FloatField(default=0.0)
    upperCircuit = models.FloatField(default=0.0)
    user = models.ManyToManyField(User, default=0)

    class Meta:

        ordering = ["companyName"]

        def __unicode__(self):

            return self.companyName

    def __str__(self) -> str:

        return self.companyName
