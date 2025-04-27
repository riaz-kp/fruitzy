
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('userAuth.urls')),
    path('',include('products.urls')),
    path('',include('category.urls')),
    path('',include('admin_panel.urls')),
    path('',include('cart.urls')),
    path('',include('orders.urls')),
    path('',include('address.urls')),
    path('',include('wishlist.urls')),
    path('',include('coupon.urls')),
    path('',include('wallet.urls')),

    path('accounts/', include('allauth.urls')),   #all auth

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
