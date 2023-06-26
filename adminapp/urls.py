from adminapp import views
from django.urls import path

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    
    
    path('add_category',views.add_category,name='add_category'),
    path('display_category',views.display_category, name="display_category"),
    path('update_category/<str:id>',views.update_category, name="update_category"),
    path('delete_category/<str:id>',views.delete_category, name="delete_category"),
    
    
    path('product_index',views.product_index,name='product_index'),
    path('add_product',views.add_product,name='add_product'),
    path('display_product',views.display_product,name='display_product'),
    path('update_product/<int:id>',views.update_product,name='update_product'),
    path('delete_product/<int:id>',views.delete_product, name="delete_product"),
    
    
    path("add_brand", views.add_brand, name="add_brand"),
    path("display_brand", views.display_brand, name="display_brand"),
    path('update_brand/<str:id>',views.update_brand, name="update_brand"),
    path('delete_brand/<str:id>',views.delete_brand, name="delete_brand"),

    
    # path('admin_index',views.admin_index,name="admin_index"),
    path('search',views.search,name="search"),
    path('display_user',views.display_user,name="display_user"),
    path('block_user/<int:id>',views.block_user, name="block_user"),
    path('unblock_user/<int:id>',views.unblock_user, name="unblock_user"),

    
]