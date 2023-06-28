from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from adminapp.models import Product
from cart.models import Cart, Cartitem, User
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum

# Create your views here.


@login_required
def add_to_cart(request,id):
    user = request.user
    #fetch product_id from 
    # product_id = request.GET.get('product_id')
    product = Product.objects.get(id=id)
    #creating cart and cartitem
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, item_created = Cartitem.objects.get_or_create( user=user,Product=product, cart=cart)
    # Check if the item already exists in the cart for the user 
    if not item_created and product.quantity > 1:
        # If the item already exists, increase its quantity by 1
        cart_item.quantity += 1
    cart_item.save()
    return redirect('home')     





    
    
@login_required(login_url="user_login")
def display_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
  
    cart_items = Cartitem.objects.filter(cart=cart)
    # subtotal=cart_items.aggregate(total=Sum('Product.selling_price'))
    print(cart_items)
    # Calculate the subtotal for each cart item
    
    context = {
        'cart_items': cart_items,
        'cart': cart,
        # 'subtotal':subtotal['total']
    }
    # if User.is_not_authenticated:
    #     return redirect('user_login')
    
    return render(request, 'user/cart.html', context)





# quantity check
# def quantity_check(request):
#     print(request.GET)
#     print("quantity check request")
#     return JsonResponse({"status":"ok"})


    
    
    
def checkout(request):
    return render(request,'user/checkout.html')