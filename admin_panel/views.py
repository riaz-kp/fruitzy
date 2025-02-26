from django.shortcuts import render,redirect
from category.models import Category
from products.models import Product
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required






@never_cache
def admin_login(request):

    if request.user.is_authenticated:
        return redirect ('home')
    
    # if request.user.is_authenticated and request.user.is_superuser:
    #     return redirect('admin_dashboard')

    
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect ('admin_dashboard')
        else:
            messages.error(request, "Username or password is incorrect.")
    return render(request,'admin/admin_login.html')


@login_required
@never_cache
def admin_logout(request):

    logout(request)
    return redirect("admin_login")

@login_required
def admin_dashboard(request):

    return render (request,'admin/dashboard.html')


@login_required
def products (request):
    # products = Product.objects.all()
    products = Product.objects.annotate(total_stock=Sum('variants__stock')).order_by('id')

    context = {
        'products' : products
    }

    return render (request,'admin/products.html',context)



@login_required
def category_list (request):
    categories = Category.objects.all()

    context = {
        'categories' : categories
    }


    return render (request,'admin/category.html', context)


