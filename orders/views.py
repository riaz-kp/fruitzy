from django.shortcuts import render
from cart.models import CartItem,Cart
from address.models import Address
def checkout(request):

    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    addresses = Address.objects.filter(user=request.user)

    context = {
        'cart_items': cart_items,
        'addresses': addresses
    }
    return render (request,'user/checkout.html', context)