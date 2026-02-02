from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(pre_save, sender=Order)
def order_status_email(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_order = Order.objects.get(pk=instance.pk)

    if old_order.status != instance.status:
        subject = f"Order #{instance.id} Status Updated"

        message = f"""
Hi {instance.user.username},

Your order status has been updated.

Order ID: {instance.id}
Previous Status: {old_order.status}
Current Status: {instance.status}

Thank you for shopping with GroceryMart!
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=False,
        )
