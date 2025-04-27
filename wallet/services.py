from django.shortcuts import render
from .models import Wallet,Ledger
from django.db import transaction




def refund_order_to_wallet(user,amount,order_id):
    wallet,created = Wallet.objects.get_or_create(user=user)

    try:
        with transaction.atomic():
            wallet.balance += amount
            wallet.save()

        Ledger.objects.create(
            wallet = wallet,
            transaction_type = 'CREDIT',
            amount = amount,
            description = f'Refund for cancelled order: #{order_id}'
        )
        return True
    
    except Wallet.DoesNotExist:
        return False
    
