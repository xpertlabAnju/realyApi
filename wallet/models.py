from django.db import models

# Create your models here.


class walletHistory(models.Model):
    transporterId = models.IntegerField(default='0')
    userId=models.IntegerField(default='0')
    orderId=models.IntegerField(default='0')
    amount=models.FloatField(default='0',blank=True, null=True)
    action=models.CharField(max_length=50)
    msg=models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete = models.SmallIntegerField(default='0')