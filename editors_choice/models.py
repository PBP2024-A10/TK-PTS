import uuid
from django.db import models
from main.models import FoodItem
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
class FoodRecommendation(models.Model):
    food_item = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    # id = food_item.id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # food_type = food_item.type
    rating = models.FloatField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_item.name
    
    def show_rating(self):
        return self.rating
    
    def validate_rating(self):
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Rating must be between 0 and 5.")
    
    # If provided, this function should return the type of the food item
    # def return_type(self):
    #     return self.food_item.type

def get_start_of_current_week():
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week
    
class EditorChoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_items = models.ManyToManyField(FoodRecommendation)
    # food_type = food_items.first().food_type
    week = models.DateField(default=get_start_of_current_week)

    def save(self, *args, **kwargs):
        if self.food_items.count() > 5:
            raise ValueError("Cannot add more than 5 food recommendations to an EditorChoice.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Editor's Choice for week starting {self.week}"
