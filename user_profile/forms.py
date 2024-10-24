from django import forms
from authentication.models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']  
