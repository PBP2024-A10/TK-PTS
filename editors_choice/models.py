import uuid
from django.db import models
from main.models import FoodItem
from cards_makanan.models import MenuItem
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
class FoodRecommendation(models.Model):
    # food_item = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    food_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    # id = food_item.id
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # food_type = food_item.type
    rating = models.FloatField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_description = models.TextField(blank=True)
    comment_count = models.PositiveIntegerField(default=0, editable=False)

    def update_comment_count(self):
        self.comment_count = self.foodcomment_set.count()
        self.save()

    def __str__(self):
        return self.food_item.name
    
    def show_rating(self):
        return self.rating
    
    def save(self, *args, **kwargs):
        self.validate_rating()
        super().save(*args, **kwargs)
    
    def validate_rating(self):
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Rating must be between 0 and 5.")

def get_start_of_current_week():
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week

class FoodComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_item = models.ForeignKey(FoodRecommendation, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} for Food: {self.food_item} at {self.timestamp}"
    
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
