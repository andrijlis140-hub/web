from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, Review

# Створюємо Inline клас для відображення товарів замовлення всередині самого замовлення
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Не додавати порожніх рядків автоматично
    readonly_fields = ('price',) # Ціну зазвичай фіксуємо, щоб вона не змінювалася випадково

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name'] # Видали 'created_at' з цього списку

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Відображаємо нові контактні дані покупця та загальну суму
    list_display = ('id', 'first_name', 'last_name', 'phone', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    
    # Додаємо товари замовлення як вбудований список
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)