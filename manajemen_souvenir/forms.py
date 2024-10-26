from django.forms import ModelForm
from manajemen_souvenir.models import SouvenirEntry
from django.utils.html import strip_tags

class SouvenirEntryForm(ModelForm):
    class Meta:
        model = SouvenirEntry
        fields = ["image", "name", "description"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
        
        