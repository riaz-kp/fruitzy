from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Variant



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"cart of {self.user.username}"

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveBigIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2,null=True ,editable=False)

    def save(self, *args, **kwargs):
        if self.variant and self.variant.product.price:
            self.item_total = self.variant.product.price * self.quantity
        super().save(*args, **kwargs)

