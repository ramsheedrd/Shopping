from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryAddView,
    CategoryEditView,
    CategoryDeleteView,
    ProductListView,
    ProductDetailView,
    ProductAddView,
    ProductEditView,
    ProductDeleteView,
    ProductImageAddView,
    ProductImageDeleteView,
    ProductFeatureAddView,
    ProductFeatureDeleteView
)

app_name = 'product'

urlpatterns = [
    path('category/', CategoryListView.as_view(), name = 'categories'),
    path('category/add/', CategoryAddView.as_view(), name='category-add'),
    path('category/get/<slug>/', CategoryDetailView.as_view(), name='category'),
    path('category/edit/<slug>/', CategoryEditView.as_view(), name='category-edit'),
    path('category/delete/<slug>/', CategoryDeleteView.as_view(), name='category-delete'),

    path('', ProductListView.as_view(), name = 'products'),
    path('product/add/', ProductAddView.as_view(), name='product-add'),
    path('product/get/<slug>/', ProductDetailView.as_view(), name='product'),
    path('product/edit/<slug>/', ProductEditView.as_view(), name='product-edit'),
    path('product/delete/<slug>/', ProductDeleteView.as_view(), name='product-delete'),
    path('product/img/add/<slug>/', ProductImageAddView.as_view(), name='product-img-add'),
    path('product/img/delete/<pk>/', ProductImageDeleteView.as_view(), name='product-img-delete'),
    path('product/feature/add/<slug>/', ProductFeatureAddView.as_view(), name='product-feature-add'),
    path('product/feature/delete/<pk>/', ProductFeatureDeleteView.as_view(), name='product-feature-delete'),



]