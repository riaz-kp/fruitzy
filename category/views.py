from django.shortcuts import render,redirect,get_object_or_404
from .models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def category_list (request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }

    return render (request,'admin/category.html', context)



@login_required
def create_category (request):

    if request.method == 'POST':
        category_name = request.POST.get('category_name').strip()
        category_offer = request.POST.get('category_offer')
        category_image = request.FILES.get('category_image')

        if Category.objects.filter(category_name__iexact=category_name).exists():
            messages.error(request, f"The category name '{category_name}' already exists.")
            return redirect('admin_category')

        category = Category.objects.create(category_name=category_name, category_image=category_image, category_offer=category_offer )
        category.save()
        return redirect('admin_category')

    return render(request,'admin/create_category.html' )





@login_required
def edit_category(request, category_id):
    # if not request.user.is_authenticated or not request.user.is_superuser:
    #     return redirect('admin_login') 
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_offer = request.POST.get('category_offer')
        category_image = request.FILES.get('category_image')


        if Category.objects.exclude(id=category_id).filter(category_name__iexact=category_name).exists():
            messages.error(request, 'Category name already exists')

            return render(request, 'admin/edit_category.html', {
                'category': category,
                'categories': Category.objects.all(),
            })

        category_name = category_name.title()  
     
        category.category_name = category_name
        category.category_offer = category_offer
        # category.category_image = category_image
        if category_image:
            category.category_image = category_image

        category.save()

        messages.success(request, 'Category updated successfully.')
        return redirect('admin_category')

    return render(request, 'admin/edit_category.html', {
        'category': category,
        'categories':Category.objects.all(),
    })



@login_required
def toggle_category_listing(request, category_id):

    # if not request.user.is_authenticated or not request.user.is_superuser:
    #     return redirect('admin_login') 
    
    category=  get_object_or_404(Category,id = category_id)
    category.is_listed = not category.is_listed
    category.save()

    return redirect('admin_category')