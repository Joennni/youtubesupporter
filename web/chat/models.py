from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
class Message(models.Model):
    auther = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.author.username
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]
    
    
class hook2(models.Model):
    username = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sense = models.TextField()