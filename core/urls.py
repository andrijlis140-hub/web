from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories),
    path('products/', views.products),
    path('category/<int:pk>/', views.category_products),
]