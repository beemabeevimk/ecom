"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    # path('<slug:category_slug>/',views.home,name='products_by_category'),
    path('signup',views.signup,name='signup'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('phone_verify',views.phone_verify, name="phone_verify"),
    path('verify_code/', views.verify_code, name="verify_code"),
    path('wireless_earbuds',views.wireless_earbuds,name='wireless_earbuds'),
    path('change_pass',views.change_pass,name='change_pass'),
    path('forgotPassword',views.forgotPassword,name='forgot_Password'),
    path('forgotPassword_otp',views.forgotPassword_otp,name='forgot_Password_otp'),
    path('resetPassword',views.resetPassword,name='resetPassword'),
    
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('address_on_profile',views.address_on_profile,name="address_on_profile"),
]

