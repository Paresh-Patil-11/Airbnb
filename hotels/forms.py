from django import forms
from .models import Hotel, Comment


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['title', 'description', 'price_per_night', 'location', 'image']
        labels = {
            'title': 'Hotel Title',
            'description': 'Description',
            'price_per_night': 'Price per Night',
            'location': 'Location',
            'image': 'Hotel Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hotel title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter hotel description'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write your comment...'
            }),
        }