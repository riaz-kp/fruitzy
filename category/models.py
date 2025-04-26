from django.db import models

class Category(models.Model):


    category_name = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='uploads/',null=True, )  # File will be stored in MEDIA_ROOT/uploads/
    is_listed = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.category_name