from django.db import models
from main.models import FoodItem
from django.conf import settings
from django.utils import timezone
import datetime

# Create your models here.
class FoodRecommendation(models.Model):
    food_item = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    # food_type = food_item.type
    rating = models.FloatField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_item.name
    
    def show_rating(self):
        return self.rating
    
    # If provided, this function should return the type of the food item
    # def return_type(self):
    #     return self.food_item.type

def get_start_of_current_week():
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week
    
class EditorChoice(models.Model):
    food_items = models.ManyToManyField(FoodRecommendation)
    # food_type = food_items.first().food_type
    week = models.DateField(default=get_start_of_current_week)

    def save(self, *args, **kwargs):
        if self.food_items.count() > 5:
            raise ValueError("Cannot add more than 5 food recommendations to an EditorChoice.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Editor's Choice for week starting {self.week}"
