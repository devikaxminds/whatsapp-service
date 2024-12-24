from django.db import models


class WhatsAppMessage(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
