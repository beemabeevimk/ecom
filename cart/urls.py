from . import views
from django.urls import path
# from django.contrib.auth import views as auth_views

urlpatterns=[
    
path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
path('display_cart',views.display_cart,name='display_cart'),
path('display_cart',views.display_cart,name='display_cart'),
# path('update_cart_item_quantity',views.update_cart_item_quantity,name='update_cart_item_quantity'),
path('checkout',views.checkout,name='checkout'),

# path('quantity_check/',views.quantity_check, name="quantity_check")

]