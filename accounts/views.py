from django.forms import PasswordInput
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout

from adminapp.models import Product,Category
from cart.models import Cartitem,Cart
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . import verify
from .forms import UserCreationForm, VerifyForm
from adminapp.models import Product,Category


# @login_required
# @verification_required
def home(request):
    products = Product.objects.all().filter(is_available=True)
    # cart = Cart.objects.filter(user=request.user).first()
    # cart_items = Cartitem.objects.filter(cart=cart)
    return render(request,'user/index.html',{'products':products})      



def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number='+91'+request.POST.get('phone')
        pass1 = request.POST.get('password')
        # pass2 = request.POST.get('confirm_password')
        # try:
        #    verify.send(phone_number)
        # except:
        #     return HttpResponse("phone number is not valid")
        myuser = CustomUser.objects.create_user(name=name,email=email,password=pass1,phone_number=phone_number)
        myuser.save()
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


