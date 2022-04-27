from rest_framework import serializers
from .models import customers

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = customers 
        fields = '__all__'