from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Images, Variant
from category.models import Category
from django.contrib import messages

import re





def user_products(request, category_id=None):
    categories = Category.objects.filter(is_listed=True)
    
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.filter(category__is_listed=True)

    return render(request, 'user/shop.html', {
        'categories': categories,
        'products': products,
        'selected_category_id': int(category_id) if category_id else None
    })






def product_desc(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    product = variant.product
 

    return render(request, 'user/product_desc.html', {'variant': variant,"product":product})



def create_product(request):

    return render(request,'admin/create_product.html')
 
def create_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        # available_stock = request.POST.get("available_stock")
        price = request.POST.get("price")
        # ripeness = request.POST.get('ripeness')
        images = request.FILES.getlist("images")
        is_listed = request.POST.get("is_listed") == "on"
        
        category = get_object_or_404(Category, id=category_id)
        
        product = Product.objects.create(
            product_name=product_name,
            description=description,
            category=category,
            price=price,
            is_listed=is_listed
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
    
    return render(request, "admin/create_product.html", {"categories": categories, "ripeness_choices": Variant.RIPENESS_CHOICES})



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
        
        product.save()

        return redirect('admin_products')

    else:
        return render(request, 'admin/edit_product.html', {
            'product': product,
            'categories': Category.objects.all(),  
            
        })
    

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


def add_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        ripeness = request.POST.get("ripeness")
        # organic = request.POST.get("organic") == "on"  # Checkbox returns "on" when checked
        stock = request.POST.get("stock")
        images = request.FILES.getlist("images")


        variant = Variant.objects.create(
            product=product,
            ripeness=ripeness,
            # organic=organic,
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
    
    


def toggle_variant_status(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    variant.is_active = not variant.is_active  # Toggle active/inactive status
    variant.save()
    messages.success(request, f"Variant status updated successfully!")
    return redirect('manage_variants', product_id=variant.product.id)