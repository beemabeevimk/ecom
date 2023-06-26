from . import views
from django.urls import path
# from django.contrib.auth import views as auth_views

urlpatterns=[
    
path('add_to_cart',views.add_to_cart,name='add_to_cart'),
path('display_cart',views.display_cart,name='display_cart'),

]