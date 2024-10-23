from django.contrib import admin
from editors_choice.models import FoodRecommendation, EditorChoice
from editors_choice.forms import FoodRecommendationForm

# Register your models here.
class FoodRecommendationAdmin(admin.ModelAdmin):
    form = FoodRecommendationForm

admin.site.register(FoodRecommendation, FoodRecommendationAdmin)