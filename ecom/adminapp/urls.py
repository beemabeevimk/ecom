from adminapp import views
from django.urls import path

urlpatterns = [
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name='admin_home'),
    # path('send_otp',views.send_otp,name='send_otp'),
    
]