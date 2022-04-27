from django.db import models

# Create your models here.
class helpandsupport(models.Model):
    subject=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    customerId=models.IntegerField(blank=True, null=True)
    fileName= models.CharField(db_column='fileName', max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)