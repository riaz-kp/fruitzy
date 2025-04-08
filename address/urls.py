

from django.urls import path
from . import views

urlpatterns = [
    path('manage_address/',views.manage_address, name='manage_address'),
    path('add_address/',views.add_address, name='add_address'),
    path('edit_address/<int:address_id>',views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>',views.delete_address, name='delete_address'),
    path('set_default_address/<int:address_id>',views.set_default_address, name='set_default_address'),

]