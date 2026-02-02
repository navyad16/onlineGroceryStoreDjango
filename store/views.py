from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404,redirect
from .models import Product,Order, OrderItem,Category
from .cart import add_to_cart, remove_from_cart, cart_items,update_quantity
from django.contrib.auth.decorators import login_required
from .utils import send_order_email
from .invoice import generate_invoice
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .forms import RegisterForm

def home(request):
    products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'home.html', {'products': products})


def products(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'products.html', {'products': products})

def add_cart(request, product_id):
    add_to_cart(request, product_id)
    return redirect('cart')

def cart(request):
    items, total = cart_items(request)
    return render(request, 'cart.html', {'items': items, 'total': total})

def remove_cart(request, product_id):
    remove_from_cart(request, product_id)
    return redirect('cart')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🔥 HASH PASSWORD
            user.set_password(form.cleaned_data['password'])

            user.save()
            return redirect('login')  # ✅ redirect to login
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def update_cart(request, product_id, action):
    update_quantity(request, product_id, action)
    return redirect('cart')

@login_required
def checkout(request):
    items, total = cart_items(request)

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'COD')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['product'].price
            )

            item['product'].stock -= item['qty']
            item['product'].save()

        send_order_email(request.user, order, items)

        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")

        return redirect('order_detail', order.id)

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return generate_invoice(order)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "This order cannot be cancelled.")
        return redirect('my_orders')

    # restore stock
    for item in order.items.all():
        product = item.product
        product.stock += item.quantity
        product.save()

    order.status = 'Cancelled'

    if order.payment_method == 'ONLINE':
        order.refund_status = 'Initiated'
    else:
        order.refund_status = 'Completed'

    order.save()

    send_mail(
        subject=f"Order #{order.id} Cancelled",
        message=f"Your order #{order.id} has been cancelled.\nRefund Status: {order.refund_status}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
    )

    messages.success(request, "Order cancelled successfully.")
    return redirect('my_orders')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'products.html', {'products': products})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })
