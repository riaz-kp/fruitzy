from django.shortcuts import render


def checkout(request):
    return render (request,'user/checkout.html')