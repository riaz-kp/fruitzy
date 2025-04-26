from django.shortcuts import render,redirect, get_object_or_404
from .models import Coupon, UserCoupon
from django.contrib import messages
from django.http import JsonResponse
from cart.models import Cart, CartItem



# admin side--------------------------------------------

def admin_coupon(request):
    coupons = Coupon.objects.all()

    return render(request, 'admin/admin_coupon.html',{'coupons':coupons})

def create_coupon(request):
    
    if request.method == 'POST':
        code = request.POST['code']
        discount_value = request.POST['discount_value']
        min_purchase_amt = request.POST['min_purchase_amt']
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to']
        usage_limit = request.POST['usage_limit']
        active = 'active' in request.POST
        if Coupon.objects.filter(code=code).exists():
            messages.error(request, 'code already exists')
            redirect ('admin_coupon')
        
        Coupon.objects.create(
            code = code,
            discount_value = discount_value,
            min_purchase_amt = min_purchase_amt,
            valid_from = valid_from,
            valid_to = valid_to,
            usage_limit = usage_limit,
            active = active
        )
        messages.success(request, 'coupon created successfully')
        return redirect('admin_coupon')

    return render(request, 'admin/create_coupon.html')


def edit_coupon(request,id):
    coupon = get_object_or_404(Coupon, id=id)
    print(coupon.valid_from)

    if request.method == 'POST':

        coupon.code = request.POST.get('code','')
        coupon.discount_value = request.POST.get('discount_value',0.00)
        coupon.min_purchase_amt = request.POST.get('min_purchase_amt', 0.00)
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.usage_limit = request.POST.get('usage_limit',1)
        coupon.active = 'active' in request.POST

        coupon.save()
        return redirect('admin_coupon')

    return render(request,'admin/edit_coupon.html' ,{"coupon":coupon})
        


# user side ----------------------------------------

def apply_coupon(request,coupon_id):
    # grand_total = total + shipping_charge - round(discount*.01)
    # total = ca

    try:
        coupon = Coupon.objects.get(id=coupon_id, active=True)
        if UserCoupon.objects.filter(user=request.user, coupon=coupon, used=True).exists():
            
            return JsonResponse({
                'success': False,
                'message': 'You have already used this coupon'
            }, status = 400
            )
        user_coupon, created = UserCoupon.objects.get_or_create(
            user=request.user,
            coupon=coupon,
            defaults={'used': False}
        )

        request.session['applied_coupon_id'] = coupon.id
        return JsonResponse({
            'success': True,
            'message': f'Coupon {coupon.code} applied successfully',
            'discount': coupon.discount_value,
            'couponCode':coupon.code
           
        },status=200)
    
    except Coupon.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid or inactive coupon'
        }, status = 404)



def remove_coupon(request):

    if 'applied_coupon_id' in request.session:
        request.session.pop('applied_coupon_id')
        messages.success(request, 'Coupon removed successfully')

    else:
        messages.warning(request, 'No coupon is applied')
        return JsonResponse({'status': 'success', 'message': 'Coupon removed'})
    return JsonResponse({'status': 'error', 'message': 'No coupon to remove'}, status=400)

