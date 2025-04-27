from django.db import models
from category.models import Category
from cloudinary.models import CloudinaryField



class Product(models.Model):

    UNIT_CHOICES = [
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
    ('ltr', 'Liter'),   
    ('packet', 'Packet'),
    ]

    product_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products" )
    # available_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_listed = models.BooleanField(default=True)
    product_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True)  # e.g., kg, packet, etc.
    product_offer = models.DecimalField(max_digits=10, null=True, decimal_places=2, blank=True)

    def __str__(self):
        return self.product_name


class Variant(models.Model):
    RIPENESS_CHOICES = [
        ('Raw', 'Raw'),
        ('Semi-Ripe', 'Semi-Ripe'),
        ('Fully-Ripe', 'Fully-Ripe'),
        
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")  # ForeignKey for relation
    ripeness = models.CharField(max_length=20, choices=RIPENESS_CHOICES, blank=True, default='Semi-Ripe', null=True)
    # organic = models.BooleanField(default=False , null=True)
    stock = models.PositiveIntegerField(default=0 , null=True)
    is_active = models.BooleanField(default=True)  

class Images(models.Model):

    # image = models.ImageField(upload_to='uploads/')
    image = CloudinaryField('image')  # Using CloudinaryField instead of ImageField
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="images")
    