from django.db import models
from django.dispatch import receiver

# Create your models here.
class rateData(models.Model):
    
    orderId=models.IntegerField() 
    userId=models.IntegerField()
    userId=models.IntegerField()
    deriverId=models.IntegerField()
    rate =models.FloatField(default='0',blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete=models.SmallIntegerField(default='0')   