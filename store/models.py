from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    refund_status = models.CharField(max_length=20, default='None')

    created_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_on = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # auto set estimated delivery
        if not self.estimated_delivery:
            self.estimated_delivery = timezone.now().date() + timedelta(days=5)

        # auto set delivered date
        if self.status == 'Delivered' and not self.delivered_on:
            self.delivered_on = timezone.now().date()

        super().save(*args, **kwargs)

    def can_cancel(self):
        return self.status in ['Pending', 'Processing']

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.product.name
