from django.db import models

# Create your models here.

class Session(models.Model):
    sessionId = models.CharField(max_length = 100)
    ownerId = models.CharField(max_length = 100)
    collaboratorId = models.CharField(max_length = 100)
