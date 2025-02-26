
from django.urls import path
from . import views

urlpatterns = [
        path('user_products/',views.user_products,name='user_products'),
        path('user_products/category/<int:category_id>/', views.user_products, name='products_by_category'),

        path('product_desc/<int:variant_id>/',views.product_desc,name='product_desc'),


        path('adminn/products/create_product/',views.create_product,name='create_product'),
        path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),  
        path('toggle-product-listing/<int:product_id>/', views.toggle_product_listing, name='toggle_product_listing'),
        path('products/<int:product_id>/variants/', views.manage_variants, name='manage_variants'),
        path('products/<int:product_id>/add_variant/', views.add_variant, name='add_variant'),
        path('variant/toggle/<int:variant_id>/', views.toggle_variant_status, name='toggle_variant_status'),


        




    
]
