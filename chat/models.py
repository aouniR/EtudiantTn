from django.db import models
from django.contrib.auth import get_user_model

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content}'

