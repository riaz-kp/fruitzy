from django.urls import path
from . import views

urlpatterns = [
        path('wallet/',views.wallet,name='wallet'),
        path('add_money_to_wallet/',views.add_money_to_wallet,name='add_money_to_wallet'),
       


]