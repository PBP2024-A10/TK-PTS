from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.Textarea(attrs={
            'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
            'rows': 1,
             }),
            'email': forms.EmailInput(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        if 'usable_password' in self.fields:
            del self.fields['usable_password'] 


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.Textarea(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
                'rows': 1,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#e8dcd4] bg-[#654a2d] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
                'rows': 1,
            })
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'block p-2.5 w-full text-sm text-[#3d200a] bg-[#e8dcd4] rounded-lg border border-[#654a2d] focus:ring-[#927155] focus:border-[#927155]',
                'placeholder': 'Write your thoughts here...',
                'rows': 4,
            }),
        }
