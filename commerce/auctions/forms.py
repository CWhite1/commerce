from django import forms
from datetime import datetime
from .models import Listings, Bids, Comments, Watchlists


class Item(forms.ModelForm):
    """Form for the image model"""
    category = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Cars, Trucks, Toys, Electronics...'} ))
    price = forms.NumberInput(attrs={"class": "form-control",'type': 'number', 'minlength': 1, 'maxlength': 15,})
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Kia, Ford, Lego, Phones...'} ))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Conditon, Size, Material, Last Used ect...', "rows": "3"}))
    required_css_class = "required-field" 
    
    class Meta:
        model = Listings
        fields = ['price', 'category', 'name', 'image', 'description']

class Bid(forms.ModelForm):
    """Form for Bid"""
    bid = forms.NumberInput(attrs={"class": "form-control",'type': 'number', 'minlength': 1, 'maxlength': 15,})
    
    class Meta:
        model = Bids
        fields = ['bid',]

class Comment(forms.ModelForm):
    """Form for Comment"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'my-textarea', 'placeholder': 'What do you think about this', "rows": "3"}))

    class Meta:
        model = Comments
        fields = ['comment',]