from django import forms
from cards_makanan.models import MenuItem
from django.forms import ModelForm, ModelChoiceField
from editors_choice.models import FoodRecommendation
from django.utils.html import strip_tags

class FoodRecommendationForm(ModelForm):
    food_item = ModelChoiceField(
        queryset=MenuItem.objects.all(),
        label='Food Item',
        help_text='Select the food item to recommend'
    )

    class Meta:
        model = FoodRecommendation
        
        fields = ['food_item', 'rating', 'rated_description']
        labels = {
            'food_item': 'Food Item',
            'rating': 'Rate the food by admin',
            'rated_description': 'Give the reason description for the rating',
        }
        help_texts = {
            'food_item': 'Select the food item to recommend',
            'rating': 'Rate the by giving a float number between 0 and 5',
            'rated_description': 'Feel free to give detailed description for the rating',
        }

    # Custom validation for rating
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError('Rating must be between 0 and 5')
        return rating
    
    # Custom validation for rated_description
    def clean_rated_description(self):
        rated_description = self.cleaned_data['rated_description']
        return strip_tags(rated_description)