def cart_count(request):
    cart = request.session.get('cart', {})
    # Рахуємо загальну кількість усіх одиниць товарів у словнику
    total_items = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_count': total_items}