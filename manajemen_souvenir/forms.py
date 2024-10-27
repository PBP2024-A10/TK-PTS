from django.forms import ModelForm
from manajemen_souvenir.models import SouvenirEntry
from django.utils.html import strip_tags
from django import forms
from django.forms import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'

class SouvenirEntryForm(ModelForm):
    class Meta:
        model = SouvenirEntry
        fields = ["name", "description","image"]
    
    image = forms.ImageField(widget=CustomClearableFileInput)

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    
        
        