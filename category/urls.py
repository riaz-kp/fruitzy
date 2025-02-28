

from django.urls import path
from . import views

urlpatterns = [
        path('adminn/category/',views.category_list,name='admin_category'),
        path('adminn/category/create_category/',views.create_category,name='create_category'),
        path('adminn/category/edit_category/<int:category_id>/',views.edit_category,name='edit_category'),
        path('adminn/category/toggle/<int:category_id>/', views.toggle_category_listing, name='toggle_category_listing'), 



    
]
