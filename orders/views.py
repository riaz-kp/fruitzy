from django.contrib import messages
from django.shortcuts import render,redirect
from cart.models import CartItem,Cart
from address.models import Address
from orders.models import Order,OrderItem

def checkout(request):

    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    addresses = Address.objects.filter(user=request.user)

    total = sum(item.item_total for item in cart_items)
    shipping_charge = 50 if total<500 else 0
    grand_total = total + shipping_charge

    for item in cart_items:
        if item.quantity > item.variant.stock:
            messages.error(request, f"{item.variant.product} {item.variant.ripeness} is available only {item.variant.stock}. Please update your cart")



    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'total' : total,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total
    }
    return render (request,'user/checkout.html', context)

def place_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        address = Address.objects.get(id=address_id)

        shipping_address = f'{address.address_name} as {address.full_name} {address.street_address} pin: {address.postal_code} Ph: {address.phone_number}'

        total = sum(item.item_total for item in cart_items)
        shipping_charge = 50 if total<500 else 0
        grand_total = total + shipping_charge    

        order = Order.objects.create(
            user = request.user,
            shipping_address = shipping_address,
            total_amount = total,
            shipping_charge = shipping_charge,
            grand_total = grand_total,
            order_status = 'pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                variant = item.variant,
                quantity = item.quantity,
                price = item.variant.product.price,
                item_total = item.item_total

            )
            item.variant.stock -= item.quantity
            item.variant.save()

        cart_items.delete()
        return redirect('order_success_page', order_id=order.order_id)



def order_success_page(request,order_id):
    return render(request, 'user/order_success_page.html', {'order_id':order_id})

def manage_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/manage_orders.html', {'orders':orders})


def order_details(request,order_id):
    order = Order.objects.get(order_id=order_id)
    return render (request, 'user/order_details.html',{'order':order})


def cancel_order(request,order_id):
    order = Order.objects.get(order_id=order_id)    
    order_items = OrderItem.objects.filter(order=order)
    order.order_status = 'cancelled'
    for item in order_items:
        item.variant.stock += item.quantity
        item.variant.save()

    order.save()
    
    return redirect('order_details',order_id=order_id)

def return_request(request,order_id):
    order = Order.objects.get(order_id=order_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        order.order_status = 'return_requested'
        order.reason_for_return = reason
        order.save()
        return redirect ("order_details", order_id=order_id)

    return render(request, 'user/return_request.html',{'order_id':order_id})

def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_orders.html',{'orders':orders})

def admin_order_details(reuqest,order_id):
    
    order = Order.objects.get(order_id=order_id)
    items = OrderItem.objects.filter(order=order)
    order_statuses = dict(Order.ORDER_STATUS)

    status_index = list(order_statuses.keys()).index(order.order_status)
    order_statuses_to_display = Order.ORDER_STATUS [status_index+1:-1] #to remove final value as requst_retrun and the current status
    print(order_statuses_to_display)

    context = {
        'order':order, 
        'items':items,
        'order_status_choices':order_statuses_to_display
        }
    
    return render(reuqest, 'admin/admin_order_details.html',context)



def change_order_status(request, order_id):
    order = Order.objects.get(order_id=order_id)

    new_status = request.POST.get('order_status')
    if new_status:
        order.order_status = new_status
        order.save()

    return redirect('admin_order_details',order_id=order_id)

