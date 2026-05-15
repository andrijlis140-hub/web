from django.db import models
from django.contrib.auth.models import User

# 1. Спочатку Категорія, щоб Product міг на неї посилатися
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

# 2. Потім Продукт
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Зображення")
    description = models.TextField(blank=True, verbose_name="Опис")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    stock = models.IntegerField(default=10, verbose_name="Залишок на складі")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

# 3. Модель Замовлення (об'єднана та розширена)
class Order(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Оплата картою'),
        ('cash', 'Оплата при отриманні'),
        ('crypto', 'Криптовалюта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    
    # Поля для форми оформлення
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100, verbose_name="Місто")
    address = models.CharField(max_length=255, verbose_name="Адреса/Відділення")

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='card', verbose_name="Спосіб оплати")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Загальна сума")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Замовлення №{self.id} від {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

# 4. Товари в замовленні
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

# 5. Кошик
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 6. Відгуки
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Рейтинг")
    text = models.TextField(blank=True, verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"