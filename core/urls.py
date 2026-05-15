from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
]



