from django import forms
from .models import Restaurant, MenuItem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Masukkan nama restoran',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Masukkan deskripsi restoran',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Masukkan lokasi restoran',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['restaurant', 'name', 'description', 'price']
        widgets = {
            'restaurant': forms.Select(attrs={
                'class': 'form-select',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Masukkan nama menu',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Masukkan deskripsi menu',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Masukkan harga menu',
                'style': 'padding: 12px; border-radius: 12px; border: 1px solid #6B7280; width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); transition: border 0.3s;',
                'onfocus': 'this.style.borderColor="#3B82F6";'
            }),
        }
