from django import forms
from .models import Products, ProductImages

class ProductImageForm(forms.Form):
    images = forms.FileField(required = False, widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category', 'product_name', 'product_price', 'description']


