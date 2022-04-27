from django.db import models

# Create your models here.
class chatDetails(models.Model):
    
    chatId=models.IntegerField()  
    senderId=models.IntegerField()
    receiverId=models.IntegerField()
    senderType = models.CharField(max_length=255, blank=True, null=True)
    receiverType = models.CharField(max_length=255, blank=True, null=True)
    messagetype = models.CharField(max_length=255, default='message', null=True)
    #chatOrderStatus :- # 0 pending , 1 withdraw , 2 accepted ,3 decline 
    chatOrderStatus = models.SmallIntegerField(default='0')
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delete=models.SmallIntegerField(default='0')    