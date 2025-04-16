from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from products.models import Product, Variant
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



@login_required
def add_to_cart (request, variant_id):
    variant= get_object_or_404(Variant, id=variant_id)
    # cart = request.user.cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, variant=variant)  #cart_item stores CartItem object and item_created Boolean (True if new item crearted False if already existed)

    cart_item.save()
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect ('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    # for item in cart_items:
    #     item.item_total=item.product.price * item.quantity

    cart_total = sum(item.variant.product.price * item.quantity for item in cart_items)
    # item_total = cart_items.product.price * cart_items.quantity


    context = {"cart_items":cart_items,
               "cart":cart,
               'cart_total':cart_total,
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
        
        quantity = int(request.POST.get('quantity',1))
        if max(1, quantity) > 10:
        
            return JsonResponse(
                {'success':False,
                 'error' : 'You cannot order more than 10 units'
                 }
            )
        elif quantity> cart_item.variant.stock:
            return JsonResponse({
                'success':False,
                'error': f"{cart_item.variant.product} {cart_item.variant.ripeness} only {cart_item.variant.stock} {cart_item.variant.product.product_unit} available"
            })
        else:
            # cart_item.quantity <= 10:
            cart_item.quantity = max(1, quantity)
            cart_item.save()
            

        item_total = cart_item.variant.product.price * cart_item.quantity
        cart_total = sum(item.variant.product.price * item.quantity for item in CartItem.objects.filter(cart=cart_item.cart))

    return JsonResponse({
            'success' : True,
            'item_total': item_total,
            'cart_total' : cart_total
        })




