from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Product, Images, Variant
from category.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from admin_panel.decorators import superuser_required
import re





def user_products(request, category_id=None):
    categories = Category.objects.filter(is_listed=True)
    
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=selected_category ,is_listed=True)
    else:
        products = Product.objects.filter(category__is_listed=True ,is_listed=True)

    return render(request, 'user/shop.html', {
        'categories': categories,
        'products': products,
        'selected_category_id': int(category_id) if category_id else None
    })






def product_desc(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    product = variant.product

    if variant.stock == 0:
        messages.error(request,'current item is out of stock')
        can_add_to_cart = False
    elif not variant.is_active:
        messages.error(request, 'current item unavailable now')
        can_add_to_cart = False
    elif variant.stock < 10:
        messages.success(request,f'only {variant.stock} available , hurry up!!!')
        can_add_to_cart = True
    else:
        can_add_to_cart= True
 
    return render(request, 'user/product_desc.html', {
        'variant': variant,
        "product":product,
        'can_add_to_cart':can_add_to_cart
        })




@login_required
@superuser_required
def products (request):
    # products = Product.objects.all()
    products = Product.objects.annotate(total_stock=Sum('variants__stock')).order_by('id')

    context = {
        'products' : products
    }

    return render (request,'admin/products.html',context)

 
@superuser_required
def create_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        # available_stock = request.POST.get("available_stock")
        price = request.POST.get("price")
        product_offer = request.POST.get('product_offer')

        # ripeness = request.POST.get('ripeness')
        images = request.FILES.getlist("images")
        # is_listed = request.POST.get("is_listed") == "on"
        
        category = get_object_or_404(Category, id=category_id)
        product_unit = request.POST.get("product_unit") 
        
        if Product.objects.filter(product_name__iexact=product_name).exists():
            messages.error(request, f"The Product name '{product_name}' already exists.")
            return redirect(create_product)
        
        
        product = Product.objects.create(
            product_name=product_name,
            description=description,
            category=category,
            price=price,
            product_offer=product_offer,
            is_listed=True,
            product_unit=product_unit,
        )
        
        variant = Variant.objects.create(
            product = product,
            ripeness = request.POST.get('ripeness'),
            # organic = request.POST.get('organic'),
            stock = request.POST.get('available_stock'),

        )

        image_objects = [Images(image=image, variant=variant) for image in images]

        if image_objects:
            Images.objects.bulk_create(image_objects)
        
        return redirect("admin_products")  
    
    categories = Category.objects.all()
    unit_choices = Product.UNIT_CHOICES
    
    return render(request, "admin/create_product.html", {"categories": categories, "ripeness_choices": Variant.RIPENESS_CHOICES, 'unit_choices': unit_choices})




@superuser_required
def edit_product(request, product_id):
    # if not request.user.is_authenticated or not request.user.is_superuser:
    #     return redirect('admin_login') 
    product = get_object_or_404(Product, id=product_id)
    errors = []
    if request.method == 'POST':
 
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        product_offer = request.POST.get('product_offer')

        if len(description) < 5:
            errors.append('Description must be less than 100 characters.')

        if float(price) < 0:
            errors.append('Price cannot be negative.')

        if re.search(r'\s', product_name):
            errors.append('Product name must not contain spaces.')


        if errors:
            return render(request, 'admin/edit_product.html', {
                'product': product,
                'categories': Category.objects.all(),
                'errors': errors,
            })
        
        product.product_name = product_name
        product.description = description
        product.category_id = category_id
        product.price = price
        product.product_offer = product_offer
        
        product.save()

        return redirect('admin_products')

    else:
        return render(request, 'admin/edit_product.html', {
            'product': product,
            'categories': Category.objects.all(),  
            
        })
    
@superuser_required
def toggle_product_listing(request, product_id):
    # if not request.user.is_authenticated or not request.user.is_superuser:
    #     return redirect('admin_login') 
    
    product = get_object_or_404(Product, id=product_id)
    product.is_listed = not product.is_listed
    product.save()
    return redirect('admin_products')


def manage_variants(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    variants = product.variants.prefetch_related('images').all()  # Fetch images with variants

    context = {
        'product': product,
        'variants' : variants
    }

    return render(request, 'admin/manage_variants.html', context)

@superuser_required
def add_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        ripeness = request.POST.get("ripeness")
        stock = request.POST.get("stock")
        images = request.FILES.getlist("images")

        if Variant.objects.filter(ripeness=ripeness).exists():
            messages.error(request, f"The '{ripeness}' already exists.")
            return redirect("manage_variants", product_id=product.id)  # Redirect to variant list
        

        variant = Variant.objects.create(
            product=product,
            ripeness=ripeness,
            stock=int(stock)
         )

        image_objects = [Images(image=image, variant=variant) for image in images]

        if image_objects:
            Images.objects.bulk_create(image_objects)
        
        return redirect("manage_variants", product_id=product.id)  # Redirect to variant list

    context = {
    "product": product,
    "ripeness_choices": Variant.RIPENESS_CHOICES  # Passing model choices
        }
    return render(request, "admin/add_variant.html", context)
    
    

@superuser_required
def toggle_variant_status(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    variant.is_active = not variant.is_active  # Toggle active/inactive status
    variant.save()
    messages.success(request, f"Variant status updated successfully!")
    return redirect('manage_variants', product_id=variant.product.id)


def edit_variant(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    product = variant.product

    if request.method == "POST":
        ripeness = request.POST.get("ripeness")
        stock = request.POST.get("stock")
        new_images = request.FILES.getlist("images")
        keep_images = request.POST.getlist("keep_images")
        delete_images = request.POST.getlist("delete_images")

        # Update variant details
        variant.ripeness = ripeness
        variant.stock = int(stock)
        variant.save()

        # Delete marked images
        if delete_images:
            Images.objects.filter(id__in=delete_images).delete()

        # Add new images
        if new_images:
            image_objects = [Images(image=image, variant=variant) for image in new_images]
            Images.objects.bulk_create(image_objects)

        messages.success(request, "Variant updated successfully.")
        return redirect("manage_variants", product_id=product.id)

    context = {
        "product": product,
        "variant": variant,
        "ripeness_choices": Variant.RIPENESS_CHOICES,
    }
    return render(request, "admin/edit_variant.html", context)