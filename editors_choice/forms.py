from django import forms
from cards_makanan.models import MenuItem
from django.forms import ModelForm, ModelChoiceField
from editors_choice.models import FoodRecommendation

class FoodRecommendationForm(ModelForm):
    food_item = ModelChoiceField(
        queryset=MenuItem.objects.all(),
        label='Food Item',
        help_text='Select the food item to recommend'
    )

    class Meta:
        model = FoodRecommendation
        
        fields = ['food_item', 'rating']
        labels = {
            'food_item': 'Food Item',
            'rating': 'Rate the food by admin'
        }
        help_texts = {
            'food_item': 'Select the food item to recommend',
            'rating': 'Rate the by giving a float number between 0 and 5'
        }

    # Custom validation for rating
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError('Rating must be between 0 and 5')
        return rating