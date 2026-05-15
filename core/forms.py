from django import forms
from .models import Order, Review



# Форма для оформлення замовлення
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'address', 'payment_method']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місто'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Відділення НП або адреса'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
        
        


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'address', 'payment_method']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Вулиця, номер будинку або № відділення'}),
            'phone': forms.TextInput(attrs={'placeholder': '+380...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 3}),
        }