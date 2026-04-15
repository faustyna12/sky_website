from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    message_type = models.CharField(max_length=25, default='sent')  

    subject = models.CharField(max_length=255)
    content = models.TextField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=25, default='sent')  
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
