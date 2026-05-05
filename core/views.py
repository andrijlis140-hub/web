from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg

from .models import Category, Product, Review
from .forms import ReviewForm


# 🏠 Головна сторінка
def home(request):
    return render(request, 'home.html')


# 📂 Категорії
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


# 📦 Всі товари
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# 🔥 Товари по категорії (Lab6)
def category_products(request, pk):
    products = Product.objects.filter(category_id=pk)
    return render(request, 'products.html', {'products': products})


# ⭐ Сторінка товару (Lab7)
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)

    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form
    })