from django.db import models

class ChatMessage(models.Model):
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message sent at {self.timestamp}"
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded at {self.timestamp}"
