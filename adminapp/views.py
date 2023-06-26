import queue
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.models import CustomUser
from django.db.models import Q
from adminapp.forms import BrandForm, CategoryForm, ProductForm, ProductImageForm
from django.http import HttpResponse
from adminapp.models import Brand, Category, Picture, Product

# from .models import Product,Category,Subcategory,ProductVariation


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('admin_home')
        else:
            messages.error(request,"Bad credentials")
    return render(request, 'admin-templates/admin-login.html')

@login_required(login_url='admin_login')
def admin_home(request):
    return render(request, "admin-templates/index.html")

@never_cache
def admin_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('admin_login')
    
    
    
# brand================================================================= 

""" hi """

@never_cache
@login_required(login_url='admin_login')
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form.save()
            return redirect('display_brand')
    else:
        form = BrandForm()
       
    return render(request, 'admin-templates/add-brand.html',{'form':form})



@login_required(login_url='admin_login')
def display_brand(request):
    if request.user.is_superuser:
        brand = Brand.objects.all()
        return render(request, 'admin-templates/display-brand.html', {'categories': brand})
    else:
        return redirect('admin_login')
    

@never_cache
@login_required(login_url='admin_login')
def update_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    # print(id)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save()
            return redirect('display_brand')
    else:
        form = CategoryForm(instance = brand)
    return render(request, "admin-templates/update-brand.html",{'form':form})  


@never_cache
@login_required(login_url='admin_login')
def delete_brand(request, id):
    get_object_or_404(Brand, id=id).delete()
    return redirect('display_brand')


    
# products==============================================================
    
    
def product_index(request):
    return render(request,"admin-templates/products-list-index.html")



@login_required(login_url='admin_login')
def display_product(request):
    products = Product.objects.all()
    return render(request, 'admin-templates/display-product.html',{'products':products})



ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, Picture, form=ProductImageForm, extra=5)
@never_cache
@login_required(login_url='admin_login')
def add_product(request):
    
    if request.method == 'POST':   
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('product_image')

        if form.is_valid():
            
            try:
                # update product table
                product = form.save()
                
                # update picture table
                for img in images:
                    new_image = Picture(product = product, image = img)
                    new_image.save()
            except Exception as e:
                print(e)
            
            return redirect('display_product')
       
    else:
        form = ProductForm()
        # image_form = ProductImageFormSet(instance=Product())
    return render(request, 'admin-templates/add-product.html', {'form': form})



@never_cache
@login_required(login_url='admin_login')
def update_product(request,id):
    product = get_object_or_404(Product, id= id)
    image_form = ImageFormSet(request.POST or None, request.FILES or None, instance=product)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid() and image_form.is_valid():
            product = form.save()
            image_form.save()
            return redirect('display_product')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin-templates/update-product.html', {'form': form, 'image_form':image_form})





@never_cache
@login_required(login_url='admin_login')
def delete_product(request, id):
    get_object_or_404(Product, id=id).delete()
    return redirect('display_product')




# category============================================================


@never_cache
@login_required(login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        # print('hi')
        if form.is_valid():
            # print("hello")
            form.save()
            return redirect('display_category')
    else:
        form = CategoryForm()
        # print('h')
    return render(request, "admin-templates/add-category.html",{'form':form})


@never_cache
@login_required(login_url='admin_login')
def display_category(request):
    categories = Category.objects.all()
    return render(request, "admin-templates/display-category.html", {'categories': categories})


@never_cache
@login_required(login_url='admin_login')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('display_category')
    else:
        form = CategoryForm(instance = category)
    return render(request, "admin-templates/update-category.html",{'form':form})



@never_cache
@login_required(login_url='admin_login')
def delete_category(request, id):
    get_object_or_404(Category, id=id).delete()
    return redirect('display_category')



# user

@login_required(login_url='admin_login')
def display_user(request):
    user = CustomUser.objects.all()
    return render(request, 'admin-templates/display-users.html', {'user':user})



def search(request):
    if request.method == 'POST':
      query = request.POST['query']
      user = CustomUser.objects.filter(queue(username__icontains=query)|Q(email__icontains=query)|Q(id__contains=query))

    return render(request,"admin_templates/search.html",{'user':user})



@never_cache
@login_required(login_url='admin_login')
def block_user(request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.is_active = False
        user.save()
        return redirect('display_user')
    
    
    
@never_cache
@login_required(login_url='admin_login')
def unblock_user(request, id):
       user = get_object_or_404(CustomUser, id = id)
       user.is_active = True
       user.save()
       return redirect('display_user')
   
   
