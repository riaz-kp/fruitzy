from django.shortcuts import render


def checkout(request):
    return render ('user/checkout.html')