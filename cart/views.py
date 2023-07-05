from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from accounts.models import Address


from adminapp.models import Product
from cart.models import Cart, Cartitem, User
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.views.generic import CreateView
# from accounts.forms import AddressForm

# Create your views here.


@login_required
def add_to_cart(request,id):
    user = request.user
    #fetch product_id from 
    # product_id = request.GET.get('product_id')
    product = Product.objects.get(id=id)
    #creating cart and cartitem
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, item_created = Cartitem.objects.get_or_create( user=user,Product=product,
                                cart=cart,total=product.selling_price*1)
    # Check if the item already exists in the cart for the user 
    if not item_created and product.quantity > 1:
        # If the item already exists, increase its quantity by 1
        cart_item.quantity += 1
    cart_item.save()
    return redirect('home')     



@login_required
def remove_cart(request, id):
    user = request.user
    cart_item = Cartitem.objects.get(id=id, user=user)
    
    # Remove the cart item from the cart
    cart_item.delete()

    return redirect('display_cart')




def update_cart_item_quantity(request):
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           cart_item = Cartitem.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            if cart_item.quantity < cart_item.Product.quantity:  # Check if quantity is less than available stock
                cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total() })


    
@login_required(login_url="user_login")
def display_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
  
    cart_items = Cartitem.objects.filter(cart=cart)
    subtotal=cart_items.aggregate(total=Sum('total'))
    print(subtotal['total'])
    # Calculate the subtotal for each cart item
    

    # if User.is_not_authenticated:
    #     return redirect('user_login')
    
    return render(request, 'user/cart.html',{'cart': cart,'cart_items': cart_items,'subtotal':subtotal['total']})





# quantity check
# def quantity_check(request):
#     print(request.GET)
#     print("quantity check request")
#     return JsonResponse({"status":"ok"})



class CheckoutView(View):

    def get(self, request):
        cart=Cart.objects.get(user=request.user)
        cart_items = Cartitem.objects.filter(user=request.user)
        subtotal=cart_items.aggregate(total=Sum('total'))
        address = Address.objects.filter(user=request.user)
        
        context = {
            'cart_items': cart_items,
            'subtotal':subtotal['total'],
            'address': address,
        }

        return render(request, 'user/checkout.html',context) 
    

# class AddAddressView(CreateView):
#     model = Address
#     form_class = AddressForm
#     template_name = 'checkout.html'

#     def form_valid(self, form):
#         form.instance.user = self.request.user

#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('checkout_view')

   
    
def display_address(request):
    return render(request,'user/add-address.html')


def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state= request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phonenumber')
        # print(request.body)
        # print(name, city, pincode, phone,address)

        address = Address.objects.create(
            user=request.user,
            name=name,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            address=address,
        )
        address.save()
        return redirect('checkout')  
    return render(request, 'user/add-address.html')



class DeleteAddressView(View):
    def get(self, request, id):
        prod = Address.objects.get(id=id)
        print(prod)
        prod.delete()
        return redirect('checkout')



def order_success(request):
    return render(request,'user/success.html')