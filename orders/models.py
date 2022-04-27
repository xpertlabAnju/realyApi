from django.db import models

# Create your models here.


class Orders(models.Model):
        fromcity = models.CharField(max_length=250)
        tocity = models.CharField(max_length=250)
        userId = models.IntegerField(default='0')
        transporterId = models.IntegerField(default='0')
        orderDescription = models.TextField(blank=True, null=True)
        statusFromUser = models.SmallIntegerField(default='0')
        # statusFromUser :- # 0 pending ,1 accepted, 2  deleted from userSide     
        OrderStatus = models.SmallIntegerField(default='0')
        #rderStatus :- # 0 pending , 1 running , 2 delivared ,3 rejected            
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        delete = models.SmallIntegerField(default='0')
        fromlatitude = models.CharField(max_length=50,blank=True, null=True)
        fromlongitude = models.CharField(max_length=50,blank=True, null=True)
        tolatitude = models.CharField(max_length=50,blank=True, null=True)
        tolongitude = models.CharField(max_length=50,blank=True, null=True)
        commision=models.FloatField(default='0',blank=True, null=True)
        finalprice=models.FloatField(default='0',blank=True, null=True)
        paymentType = models.TextField(blank=True, null=True)  # Field name made lowercase.
        isRequested = models.SmallIntegerField(default='0')
        paid= models.SmallIntegerField(default='0') 
        amount=models.FloatField(default='0',blank=True, null=True)


class Orderdetails(models.Model):
    orderid = models.BigIntegerField(db_column='orderId', blank=True, null=True)  # Field name made lowercase.
    userId = models.BigIntegerField(blank=True, null=True)
    transporterid = models.BigIntegerField(blank=True, null=True)
    messagetype = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    messagetime = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete = models.SmallIntegerField(default='0')
    senderType = models.CharField(max_length=255, blank=True, null=True)
    receiverType = models.CharField(max_length=255, blank=True, null=True)
