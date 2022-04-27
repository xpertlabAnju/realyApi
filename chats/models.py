from django.db import models

# Create your models here.

class chat(models.Model):
    orderId=models.IntegerField()  
    userId=models.IntegerField()
    transporterId=models.IntegerField()
    amount=models.FloatField(default='0',blank=True, null=True)
    # 0=accepted,1=completed
    driverstatus=models.IntegerField(default='0')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete=models.SmallIntegerField(default='0')  
