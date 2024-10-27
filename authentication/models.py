from django.db import models
import uuid
from django.contrib.auth.models import User

class ProductEntry(models.Model):
    wishlist_users = models.ManyToManyField(User, related_name='wishlist_items', blank=True)

