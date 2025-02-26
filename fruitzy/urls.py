
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('userAuth.urls')),
    path('',include('products.urls')),
    path('',include('category.urls')),
    path('adminn/',include('admin_panel.urls')),
    path('accounts/', include('allauth.urls')),   #all auth


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
