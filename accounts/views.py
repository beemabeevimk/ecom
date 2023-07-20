from django.forms import PasswordInput
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from accounts.models import Address, CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout

from adminapp.models import Product,Category
from cart.models import Cartitem,Cart, Orders
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import verify
from .forms import UserCreationForm, VerifyForm
from adminapp.models import Product,Category
from twilio.rest import Client
import random   


# @login_required
# @verification_required
def home(request):
    products = Product.objects.all().filter(is_available=True)
    # cart = Cart.objects.filter(user=request.user).first()
    # cart_items = Cartitem.objects.filter(cart=cart)
    return render(request,'user/index.html',{'products':products})      




def signup(request):
    print("signup")
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number='+91'+request.POST.get('phone')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirmpassword')
        
        if pass1 != pass2:
            return render(request,"user/signup.html",{"error":"password missmach"})
        
        try:
            print("post creatre")
            myuser = CustomUser.objects.create_user(name=name,email=email,password=pass1,phone_number=phone_number)
            print("user created")
        except Exception as e:
            print("exception found!")
            return render(request,"user/signup.html",{"error":"email already exist!"})
        
        return redirect("user_login")
    return render(request,"user/signup.html")




def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['register-email']
        password = request.POST['register-password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
           auth_login(request,user)
           return redirect('home')
        else:
            messages.error(request,"User name or password is incorect")
    return render(request,"user/login.html")


def user_logout(request):
    logout(request)
    return redirect('user_login')



def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone')
            
            if verify.check(phone_no, code):
                user = CustomUser.objects.get(email=request.session.get('email')) 
                userobj = CustomUser.objects.filter(email=request.session.get('email')) 
                print(user)
                print(user.is_authenticated)
                print(user.is_active)
                print(user.is_superuser)
                if userobj.exists() and user.is_active and not user.is_superuser: 
                    print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect('home')  
                # print(user)
                return redirect('home') 
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'user/verify.html', {'form': form})




def phone_verify(request):
    if request.method == "POST":
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(phone):
            
            verify.send(phone)
            
            user = username_password(phone)
            request.session['email'] = user.email 
            print(user.email)  
            user.is_verified = True
            user.is_active = True
            user.save()
            request.session['phone'] = phone
            return redirect('verify_code') 
        else:
            context = "Please register first"
            return render(request, 'user/phone_verify.html', {'context': context})
    return render(request, 'user/phone_verify.html')






def forgotPassword(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        print("enterd")
        
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        print(mobile_number_forgotPassword)
        
        # checking the null case
        if mobile_number_forgotPassword is '':
            print("nothappen")
            # messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        
        
        user = CustomUser.objects.filter(phone_number = '+91'+  str(mobile_number_forgotPassword))
        print(user)
            
        if user:  #if user exists
            verify.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgot_Password_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgot_Password')
            
    return render(request, 'user/phone_verify.html')



def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    print(mobile_number)
    
    if request.method == 'POST':
          
        form = VerifyForm(request.POST)
        if form.is_valid():
             otp  = form.cleaned_data.get('code')
        if verify.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number='+91'+  str(mobile_number))
            if user:
                return redirect('resetPassword')
        else:
            # messages.warning(request,'Invalid OTP')
            return redirect('forgot_Password_otp')
    else:
        form = VerifyForm()

        
    return render(request, 'user/verify.html', {'form': form})




def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number='+91'+ str(mobile_number))
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            # messages.success(request, 'Password changed successfully')
            return redirect('user_login')
        else:
            # messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'user/resetpassword.html')





def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    return user

def check_phone_number(phone_number):
    return CustomUser.objects.filter(phone_number=phone_number).first()


def wireless_earbuds(request):
    products = Product.objects.all().filter(category_id=1,is_available=True)
    return render(request,'user/wireless_earbuds.html',{'products':products})
    

def change_pass(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone')
            
            if verify.check(phone_no, code):
                # print("checked")
                
                user = CustomUser.objects.get(email=request.session.get('email')) 
                userobj = CustomUser.objects.filter(email=request.session.get('email')) 
                if userobj.exists() and user.is_active and not user.is_superuser: 
                    # print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect('home')  
                return redirect('home') 
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'user/verify.html', {'form': form})


def new_pass(request):
    return render('change-pass.html')


def user_profile(request):
    user = request.user
    address = Address.objects.filter(user=user)
    orders = Orders.objects.filter(user=request.user).order_by("-created_at")
    # orders = Orders.objects.all().order_by("-created_at")
    return render(request,'user/dashboard.html',{'user':user,'address':address,'orders':orders})

def edit_profile(request):
    return render(request,'user/edit-profile.html')


def address_on_profile(request):
    return render(request,'user/address-profile.html')