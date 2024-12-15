from django.contrib.auth.models import User
from django.db import models
from cards_makanan.models import MenuItem
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)