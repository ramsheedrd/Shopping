from django import forms

class ProductImageForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))