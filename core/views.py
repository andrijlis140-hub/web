from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib import messages
from .models import Category, Product, Review, Order, OrderItem
from .forms import ReviewForm, OrderCreateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# --- ГОЛОВНІ СТОРІНКИ ТА КАТЕГОРІЇ ---

def home(request):
    """Головна сторінка."""
    products_list = Product.objects.all()
    # Додаємо категорії в контекст, якщо вони потрібні для навігації
    return render(request, 'registration/home.html', {'products': products_list})

def products(request):
    return redirect('home')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'registration/categories.html', {
        'category': category,
        'products': products
    })

def categories(request):
    categories_list = Category.objects.all()
    return render(request, 'registration/categories.html', {'categories': categories_list})

# --- РЕЄСТРАЦІЯ ---

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Вітаємо, {user.username}! Ви успішно зареєструвалися.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- ДЕТАЛІ ТОВАРУ ---

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    
    user_already_reviewed = False
    if request.user.is_authenticated:
        user_already_reviewed = Review.objects.filter(product=product, user=request.user).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Будь ласка, увійдіть, щоб залишити відгук.")
            return redirect('login')

        if user_already_reviewed:
            messages.error(request, "Ви вже залишили відгук до цього товару.")
            return redirect('product_detail', pk=pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Ваш відгук додано!")
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'registration/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'user_already_reviewed': user_already_reviewed,
    })

# --- ЛОГІКА КОШИКА ---

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Захист від дивних типів даних у сесії
    if not isinstance(cart, dict):
        cart = {}
        
    p_id = str(product_id)
    cart[p_id] = cart.get(p_id, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, "Товар додано до скарбниці! 🧺")
    
    # Повертаємо на ту саму сторінку, де був користувач
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        del cart[p_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Товар видалено.")
    
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products_in_cart = []
    total_cart_price = 0

    for p_id, quantity in cart.items():
        try:
            # Явно приводимо до int для надійності
            product = Product.objects.get(id=int(p_id))
            product_total = product.price * quantity
            total_cart_price += product_total
            
            # Додаємо тимчасові атрибути для шаблону
            product.quantity = quantity
            product.total_price = product_total
            products_in_cart.append(product)
        except (Product.DoesNotExist, ValueError):
            continue

    return render(request, 'registration/cart.html', {
        'products': products_in_cart,
        'total_cart_price': total_cart_price,
    })

# --- ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ---

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Ваш кошик порожній!")
        return redirect('cart_detail')
    
    total_cart_price = 0
    cart_items_data = [] 
    
    for p_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(p_id))
            total_cart_price += product.price * quantity
            cart_items_data.append({'product': product, 'quantity': quantity})
        except (Product.DoesNotExist, ValueError):
            continue
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = total_cart_price
            order.save()

            for item in cart_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            # Очищення кошика після успіху
            request.session['cart'] = {}
            request.session.modified = True
            
            messages.success(request, f"Дякуємо, {order.first_name}! Замовлення №{order.id} оформлено.")
            return redirect('home')
    else:
        form = OrderCreateForm()
        
    return render(request, 'registration/checkout.html', {
        'form': form,
        'total_cart_price': total_cart_price,
        'cart_items': cart_items_data
    })