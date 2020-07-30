from django.contrib import admin
from .models import (
    Categories,
    Products,
    ProductImages,
    ProductFeatures
)

# Register your models here.

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(ProductImages)
admin.site.register(ProductFeatures)
