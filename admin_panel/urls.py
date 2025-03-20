
from django.urls import path
from . import views

urlpatterns = [
        path('adminn/',views.admin_dashboard,name='admin_dashboard'),
        path('adminn/admin_login', views.admin_login,name='admin_login'),
        path('adminn/admin_logout', views.admin_logout,name='admin_logout'),

]   
