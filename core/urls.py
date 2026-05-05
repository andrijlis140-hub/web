from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories),
    path('products/', views.products),
    path('category/<int:pk>/', views.category_products),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]