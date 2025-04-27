
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Wallet

User = get_user_model()   #to make flexible for custom users

def create_wallet_for_new_user(sender, instance,created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


