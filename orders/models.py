from django.db import models
from django.contrib.auth.models import User
from products.models import Variant
import uuid
from coupon.models import Coupon,UserCoupon

# Create your models here.

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash_on_delivery','cash_on_delivery'),
        ('razor_pay','razor_pay'),
        ('wallet', 'wallet')
    ]
    ORDER_STATUS = [
        ('pending','pending'),
        ('order_confirmed','order confirmed'),
        ('order_shipped','order shipped'),
        ('out_of_delivery','out of delivery'),
        ('cancelled','cancelled'),
        ('delivered','delivered'),
        ('return_requested','return requested'),
        ('returned','returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    reason_for_return = models.TextField(null=True, blank=True)
    applied_coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE , null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.order_id:
            uid = uuid.uuid4().hex[:8].upper()
            self.order_id = f"ORD{uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)





    