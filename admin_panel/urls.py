
from django.urls import path
from . import views

urlpatterns = [
        path('',views.admin_dashboard,name='admin_dashboard'),
        path('admin_login', views.admin_login,name='admin_login'),
        path('admin_logout', views.admin_logout,name='admin_logout'),
        path('products/',views.products,name='admin_products'),
        path('category/',views.category_list,name='admin_category'),

]   
