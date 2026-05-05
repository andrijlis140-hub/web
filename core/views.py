from django.shortcuts import render
from .models import Category, Product

def home(request):
    return render(request, 'home.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def category_products(request, pk):
    products = Product.objects.filter(category_id=pk)
    return render(request, 'products.html', {'products': products})
