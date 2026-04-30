# Author: Faustyna Szulc (w2081508)
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages') #foreign key to User model for sender of the message
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages') #foreign key to User model for receiver of the message
    
    message_type = models.CharField(max_length=25, default='sent')  

    subject = models.CharField(max_length=255)
    content = models.TextField()
    
    timestamp = models.DateTimeField(auto_now_add=True) #timestamp for when the message was created, automatically set to current time when message is created
    
    status = models.CharField(max_length=25, default='sent')  
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.subject 
