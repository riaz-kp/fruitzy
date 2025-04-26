

from django.urls import path
from . import views

urlpatterns = [
        path('adminn/admin_coupon/',views.admin_coupon,name='admin_coupon'),
        path('adminn/create_coupon/',views.create_coupon,name='create_coupon'),
        path('adminn/edit_coupon/<int:id>/',views.edit_coupon,name='edit_coupon'),

        path('apply_coupon/<int:coupon_id>/',views.apply_coupon, name='apply_coupon'),
        # path('apply_coupon/<int:coupon_id>/'),

        path('remove_coupon/',views.remove_coupon, name='remove_coupon'),


    
]

