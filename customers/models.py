from django.db import models

# Create your models here.

class customers(models.Model):
 
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50)
    number = models.CharField(max_length=15, blank=True, null=True,default='0')
    email = models.CharField(max_length=100)
    otp = models.IntegerField(default='0')
    profilepic = models.CharField(max_length=100, blank=True, null=True)
    allownotification = models.SmallIntegerField(db_column='allowNotification', null=True,default='0')  # Field name made lowercase.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete = models.SmallIntegerField(default='0')
    type = models.SmallIntegerField(default='0')
    status = models.SmallIntegerField(blank=True, null=True,default='0')
    isrequested = models.SmallIntegerField(db_column='isRequested',default='0')  # Field name made lowercase.
    document = models.CharField(max_length=200, blank=True, null=True)
    rejectionreason = models.TextField(db_column='rejectionReason', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(blank=True, null=True)
    walletamount=models.FloatField(default='0',blank=True, null=True)
    withdrawamount=models.FloatField(default='0',blank=True, null=True)
