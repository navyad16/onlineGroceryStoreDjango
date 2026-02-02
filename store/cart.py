from .models import Product
from django.shortcuts import get_object_or_404

def get_cart(request):
    return request.session.setdefault('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        return

    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1

    save_cart(request, cart)

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    save_cart(request, cart)
def update_quantity(request, product_id, action):
    cart = get_cart(request)
    pid = str(product_id)

    if pid in cart:
        if action == 'increase':
            cart[pid] += 1
        elif action == 'decrease':
            cart[pid] -= 1
            if cart[pid] <= 0:
                del cart[pid]

    save_cart(request, cart)


def cart_items(request):
    cart = get_cart(request)
    items = []
    total = 0

    products = Product.objects.filter(id__in=cart.keys())

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        total += subtotal

        items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal
        })

    return items, total


