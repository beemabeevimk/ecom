from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from adminapp.models import Product
from cart.models import Cart, Cartitem, User
from django.http import HttpResponse, JsonResponse

# Create your views here.


@login_required
def add_to_cart(request):
    user = request.user
    #fetch product_id from 
    product_id = request.GET.get('product_id')
    product = Product.objects.get(pk=product_id)
    #creating cart and cartitem
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, item_created = Cartitem.objects.get_or_create( user=user,Product=product, cart=cart)
    # Check if the item already exists in the cart for the user 
    if not item_created and product.quantity_in_stock > 1:
        # If the item already exists, increase its quantity by 1
        cart_item.quantity += 1
    cart_item.save()
    
    
@login_required(login_url="user_login")
def display_cart(request):

    cart = Cart.objects.filter(user=request.user).first()
  
    cart_items = Cartitem.objects.filter(cart=cart)

    # Calculate the subtotal for each cart item
    
    context = {
        'cart_items': cart_items,
        'cart': cart
    }
    # if User.is_not_authenticated:
    #     return redirect('user_login')
    
    return render(request, 'user/cart.html', context)



@login_required          
def update_cart_item_quantity(request):
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           cart_item = Cartitem.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total })    