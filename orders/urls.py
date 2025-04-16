from django.urls import path
from . import views

urlpatterns = [
        path('checkout/',views.checkout,name='checkout'),
        path('place_order', views.place_order, name= 'place_order'),
        path('order_success_page/<str:order_id>/', views.order_success_page, name= 'order_success_page'),
        path('manage_orders',views.manage_orders, name='manage_orders'),
        path('order_details/<str:order_id>',views.order_details,name='order_details'),
        path('cancel_order/<str:order_id>',views.cancel_order,name='cancel_order'),
        path('return_request/<str:order_id>',views.return_request,name='return_request'),
        path('admin_orders',views.admin_orders, name='admin_orders'),
        path('admin_order_details/<str:order_id>',views.admin_order_details,name='admin_order_details'),
        path('change_order_status/<str:order_id>',views.change_order_status,name='change_order_status'),




]