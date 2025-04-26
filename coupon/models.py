from django.db import models
from django.utils import timezone
from django.contrib.auth.models  import User


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amt = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveBigIntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Coupon {self.code} -- {self.discount_value}"

    def is_valid (self):
        now = timezone.now().date()
        return self.active and self.valid_from <= now <= self.valid_to


class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='user_coupon')
    used = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} === {self.coupon.code}"

    def can_use(self):
        return not self.used and self.coupon.is_valid()