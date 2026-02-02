from django.core.mail import send_mail
from django.conf import settings

def send_order_email(user, order, items):
    product_list = ""
    for item in items:
        product_list += f"- {item['product'].name} × {item['qty']}\n"

    subject = f"🛒 Order #{order.id} Confirmed"

    message = f"""
Hi {user.username},

✅ Your order has been placed successfully!

Order ID: {order.id}
Total Amount: ₹{order.total_amount}
Payment Method: {order.payment_method}
Status: {order.status}

📦 Products:
{product_list}

🚚 Estimated Delivery: {order.estimated_delivery}

Thank you for shopping with GroceryMart 🙏
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False  # IMPORTANT
    )
