from django.db import models

# Create your models here.
class content(models.Model):

	key=models.CharField(max_length=100)
	value=models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)