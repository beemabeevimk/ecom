from . import views
from django.urls import path
from .views import CheckoutView, DeleteAddressView
# from django.contrib.auth import views as auth_views
# from .views import PlaceOrderView


urlpatterns=[
    
path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
path('display_cart',views.display_cart,name='display_cart'),
path('display_cart',views.display_cart,name='display_cart'),
path('update_cart_item_quantity',views.update_cart_item_quantity,name='update_cart_item_quantity'),

path('checkout',CheckoutView.as_view(),name='checkout'),
path('payment_page/<int:id>/',views.payment_page,name='payment_page'),
path('add_address',views.add_address,name='add_address'),
path('display_address',views.display_address,name='display_address'),
path('delete_address/<int:id>/', DeleteAddressView.as_view(), name='delete_address'),

path('order_success',views.order_success,name='order_success'),
path('remove_cart/<int:id>/',views.remove_cart,name='remove_cart'),

 path('order',views.order,name='order'),
 
 path('orderpage',views.orderpage,name="orderpage"),

]