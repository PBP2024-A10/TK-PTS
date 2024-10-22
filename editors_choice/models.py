from django.db import models
from main.models import FoodItem

# Create your models here.
class EditorRecommendation(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_item.name