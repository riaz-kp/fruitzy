from django.contrib import messages
from django.shortcuts import render,redirect
from cart.models import CartItem,Cart
from address.models import Address
from orders.models import Order,OrderItem
from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
from weasyprint import HTML
from django.template.loader import render_to_string
from coupon.models import Coupon, UserCoupon
from django.utils import timezone



def checkout(request):

    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    addresses = Address.objects.filter(user=request.user)
    total = sum(item.item_total for item in cart_items)
    shipping_charge = 50 if total<500 else 0

    discount = 0
    applied_coupon = None 

    # coupon_id = request.session.get('applied_coupon_id')
    # coupon_id = UserCoupon.objects.get()
    coupon_id = request.GET.get('applied_coupon_id')  

    if coupon_id:
        try:
            applied_coupon = Coupon.objects.get(id=coupon_id)
            already_used = UserCoupon.objects.filter(user=request.user, coupon=applied_coupon, used=True).exists()

            print("applied coupon is: ",already_used)

            if applied_coupon.is_valid() and not already_used and total >= applied_coupon.min_purchase_amt:
                discount = applied_coupon.discount_value
            # else:
            #     request.session.pop('applied_coupon_id', None)

            print("discount is: ",discount)
        except Coupon.DoesNotExist:
            pass
    available_coupons = Coupon.objects.filter(active=True).exclude(
        user_coupon__user=request.user,
        user_coupon__used=True
    )

        # available_coupons = [coupon for coupon in available_coupons if coupon.is_valid()]
    available_coupons = [
        coupon for coupon in available_coupons
        if coupon.is_valid() and total >= coupon.min_purchase_amt
    ]


    grand_total = total + shipping_charge - discount
    # grand_total = 0
    
    for item in cart_items:
        if item.quantity > item.variant.stock:
            messages.error(request, f"{item.variant.product} {item.variant.ripeness} is available only {item.variant.stock}. Please update your cart")

    print("applied coupon:",applied_coupon)
    print("grant total: ",grand_total)


    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'total' : total,
        'applied_coupon': applied_coupon,
        'available_coupons': available_coupons,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total
    }
    return render (request,'user/checkout.html', context)



def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        address_id = request.POST.get('address')
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

    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(order_id__icontains=query, user=request.user)
    else:
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
    items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        order.order_status = 'return_requested'
        order.reason_for_return = reason

        for item in items:
            item.variant.stock += item.quantity
            item.variant.save()

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
    order_statuses_to_display = Order.ORDER_STATUS [status_index+1:]     
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



def generate_invoice_pdf(request,order_id):
    
    order = Order.objects.get(order_id=order_id)
    items = OrderItem.objects.filter(order=order)
    context = {'order':order, 'items':items}
    
    html_string = render_to_string('user/invoice2.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}"'
    return response
