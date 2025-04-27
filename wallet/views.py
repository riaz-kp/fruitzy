from django.shortcuts import render
from .models import Wallet,Ledger
from django.db import transaction


def wallet(request):
    wallet,created = Wallet.objects.get_or_create(user=request.user)
    transactions = Ledger.objects.filter(wallet=wallet).order_by('-created_at')


    return render(request, 'user/wallet.html', {'wallet':wallet, 'transactions':transactions})


def add_money_to_wallet(request):
    pass


