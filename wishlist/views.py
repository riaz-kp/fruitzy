from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from products.models import Product
from .models import Wishlist, WishlistItems


def wishlist(request):
    wishlist, created =Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = WishlistItems.objects.filter(wishlist=wishlist)

    return render(request, 'user/wishlist.html', {'wishlist_items':wishlist_items})

def add_to_wishlist(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    wishlist, created =Wishlist.objects.get_or_create(user=request.user)
    wishlist_item,item_created =WishlistItems.objects.get_or_create(wishlist=wishlist, product=product)


    if not item_created:
        return JsonResponse({
        'success':False,
        'message':"Item already in wishlist"
    })
    else:   
        wishlist_item.save()
        return JsonResponse({
            'success':True,
            'message':"Item added to wishlist successfully"
        })




def remove_from_wishlist(request,item_id):
    wishlist_item = get_object_or_404(WishlistItems, id=item_id, wishlist__user=request.user)
    wishlist_item.delete()

    return redirect ('wishlist')

    