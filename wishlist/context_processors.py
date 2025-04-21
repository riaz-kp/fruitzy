from .models import Wishlist

def wishlist_items_count(request):
    count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            count = wishlist.items.count()
    return {'wishlist_items_count': count}