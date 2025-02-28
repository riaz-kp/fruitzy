
from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
        path('login',views.user_login,name='user_login'),
        path('signup',views.user_signup,name='user_signup'),
        path('logout/', views.user_logout, name='user_logout'),
        path('adminn/user_management/', views.user_management, name='user_management'),
        path('adminn/block_unblock_user <int:user_id>/', views.block_unblock_user, name='block_unblock_user'),

        path('',views.home,name='home'),
        path('about',views.about,name='about'),
    
]


handler404 = views.custom_404_view
