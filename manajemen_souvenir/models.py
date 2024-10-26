from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class SouvenirEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name