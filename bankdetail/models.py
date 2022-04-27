from django.db import models

# Create your models here.
class bankdetail(models.Model):
    
    userId = models.BigIntegerField(blank=True, null=True)
    bankname = models.CharField(max_length=255, blank=True, null=True)
    accountname = models.CharField(max_length=255, blank=True, null=True)
    accountnumber = models.BigIntegerField(blank=True, null=True)
    ifccode = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete = models.SmallIntegerField(default='0')