from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from .models import (
    Categories,
    Products,
    ProductImages,
    ProductFeatures
)
from .forms import ProductImageForm

# Create your views here.

# category views

class CategoryListView(ListView):
    model = Categories
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Categories
    context_object_name = 'category'


class CategoryAddView(CreateView):
    model = Categories
    fields = ['category_name', 'category_image']
    template_name_suffix = '_add_form'
    success_url = reverse_lazy('product:categories')


class CategoryEditView(UpdateView):
    model = Categories
    fields = ['category_name', 'category_image']
    template_name_suffix = '_edit_form'


class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = reverse_lazy('product:categories')


# product views

class ProductListView(ListView):
    model = Products
    context_object_name = "products"
    

class ProductDetailView(DetailView):
    model = Products
    context_object_name = 'product'


class ProductAddView(CreateView):
    model = Products
    fields = ['category', 'product_name', 'product_price', 'description']
    template_name_suffix = '_add_form'


class ProductEditView(UpdateView):
    model = Products
    fields = ['category', 'product_name', 'product_price', 'description']
    template_name_suffix = '_edit_form'


class ProductDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('product:products')


class ProductImageAddView(FormView):
    form_class = ProductImageForm
    template_name = 'product/product_image_add_form.html'  # Replace with your template.

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product = get_object_or_404(Products, slug = kwargs.get("slug"))
        images = request.FILES.getlist('images')
        if form.is_valid():
            for f in images:
                instance = ProductImages(product=product, image= f)  # match the model.
                instance.save()
            return redirect(product.get_absolute_url())
        else:
            return self.form_invalid(form)


class ProductImageDeleteView(DeleteView):
    model = ProductImages

    def get_success_url(self):
        image = get_object_or_404(ProductImages, pk=self.kwargs.get("pk"))
        return reverse('product:product', kwargs = {'slug': image.product.slug })


class ProductFeatureAddView(CreateView):
    model = ProductFeatures
    fields = ['feature']
    template_name_suffix = '_add_form'

    def form_valid(self, form):
        # self.object = form.save()
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Products, slug = slug)
        temp = form.save(commit=False)
        temp.product = product
        temp.save()
        return redirect(product.get_absolute_url())


class ProductFeatureDeleteView(DeleteView):
    model = ProductFeatures

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        feature = get_object_or_404(ProductFeatures, pk=self.kwargs.get("pk"))
        return reverse('product:product', kwargs = {'slug': feature.product.slug })