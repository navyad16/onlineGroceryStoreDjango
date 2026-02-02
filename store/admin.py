from django.contrib import admin
from .models import Category, Product,Order
from .utils import send_order_email

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'payment_method',
        'refund_status',
        'created_at'
    )
    list_editable = ('status', 'refund_status')

    def save_model(self, request, obj, form, change):
        old_status = None

        if obj.pk:
            old_status = Order.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        # 🔔 Send email ONLY if status changed
        if old_status != obj.status:
            send_order_email(obj.user, obj)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)