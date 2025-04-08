from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Address(models.Model):
    address_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    street_address = models.TextField()
    postal_code = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def save(self, *args , **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True)

        super().save(*args, **kwargs)


    def set_default(self):
        Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

    def __str__(self):
        return f"{self.address_name}"

        