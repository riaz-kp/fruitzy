from django.shortcuts import render, get_object_or_404,redirect
from products.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart (request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # cart = request.user.cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)  #cart_item stores CartItem object and item_created Boolean (True if new item crearted False if already existed)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect ('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    context = {"cart_items":cart_items,
               "cart":cart,
               'cart_total':cart_total
               }
    return render(request, "user/cart.html", context)


@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404 (CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def update_cart(request,item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity',1))
        cart_item.quantity = max(1, new_quantity)
        cart_item.save()

    return redirect('view_cart')



