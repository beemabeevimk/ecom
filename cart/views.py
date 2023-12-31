from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
import razorpay
from accounts.models import Address


from adminapp.models import Product
from cart.models import Cart, Cartitem, OrderProduct, Orders, Payment, User
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.forms.models import model_to_dict
# from django.views.generic import CreateView
# from accounts.forms import AddressForm
from django.conf import settings





def calculate_total(request):
    cart_items = Cartitem.objects.filter(user=request.user)  # Assuming you have a CartItem model with a user field
   
    # Calculate the subtotal for each cart item
    subtotal_list = [item.quantity * item.total for item in cart_items]

    # Calculate the total by summing up the subtotals
    total = sum(subtotal_list)   
   
    return total   



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
        subtotal=calculate_total(request)
        print(subtotal)
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total(),"total_total":subtotal })



  





    
@login_required(login_url="user_login")
def display_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
  
    cart_items = Cartitem.objects.filter(cart=cart)
    subtotal=calculate_total(request)
    print(subtotal)
    # Calculate the subtotal for each cart item
    # if User.is_not_authenticated:
    #     return redirect('user_login')
    
    return render(request, 'user/cart.html',{'cart': cart,'cart_items': cart_items,"total_total":subtotal})







# quantity check
# def quantity_check(request):
#     print(request.GET)
#     print("quantity check request")
#     return JsonResponse({"status":"ok"})



class CheckoutView(View):

    def get(self, request):
        cart=Cart.objects.get(user=request.user)
        cart_items = Cartitem.objects.filter(user=request.user)
        # subtotal=cart_items.aggregate(total=Sum('total'))
        subtotal=calculate_total(request)
        address = Address.objects.filter(user=request.user)
        # print(address)
        
        context = {
            'cart_items': cart_items,
            # 'subtotal':subtotal['total'],
            'address': address,
            "total_total":subtotal,
             'cart':cart.cart_id,
             
        }

        return render(request, 'user/checkout.html',context) 
    
    
    
    
    
    
    
def payment_page(request,id):
    cart_items = Cartitem.objects.filter(user=request.user)
    subtotal=calculate_total(request)
    # address = Address.objects.filter(user=request.user)
    address = Address.objects.get(id=id)
    
    context = {
            'cart_items': cart_items,
            # 'subtotal':subtotal['total'],
            'address': address,
            "total_total":subtotal,
        }
    return render(request,'user/payment.html',context)
    

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
    order_id = request.GET.get('order_id')
  
    orders1 = request.GET.get('orders')
    print(orders1)
    ordered_products = OrderProduct.objects.filter(order_id=orders1)  
    orders = Orders.objects.filter()           
    # order = get_object_or_404(Orders, id=order_id)
    order = OrderProduct.objects.get(id=order_id)
    print(order)
    product = order.product
    product_dict = model_to_dict(product)    
    # Access the fields from the related Product model
    product_image = product_dict['product_image'].url
    selling_price = product_dict['selling_price']
    # Retrieve other fields from the OrderProduct model
    user = order.user
    address = order.address
    ordered = order.ordered
    is_paid = order.is_paid
    status = order.status
    quantity = order.quantity
    payment = order.payment      
    context = {
        'order_id': order_id,
        'quantity': quantity,
        'product_price':selling_price,
        'product_name': product_dict['name'],
        'ordered':ordered,
        'is_paid':is_paid,
        'user': str(user),
        'address':address,
        'status':status,
        'product':product,
        'payment':payment,
        'image_url':product_image,
        'ordered_products': ordered_products,
    }                                    
    return render(request,'user/success1.html',context)
    
    

#ajax method to create order
def order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('paymentmethod')
        
        if payment_method == "Razor Payment":
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            amount=request.POST.get('grandPriceText')
            grand_total = int(amount)
            

# Print the datatype
            print(amount)
            razor_payment = client.order.create({ "amount": grand_total*100, "currency": "INR", "receipt": "order_rcptid_11" })
            print(razor_payment)
            print(razor_payment['id'])
            cart_items = Cartitem.objects.filter(user=request.user)
            address = request.POST.get('address')
            address_details = Address.objects.get(id=address)

            payment = Payment.objects.create(
                user=request.user,
                payment_method=request.POST.get('paymentmethod'),
                amount=request.POST.get('grandPriceText'),
            )
            payment.save()

            order = Orders.objects.create(
                user=request.user,
                payment=payment,
                address=address_details,
                ordered=False,
                status="New",
                quantity=False,
            )
            order.save()

            for cart_item in cart_items:
                ordered_product = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.Product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.Product.selling_price,
                    ordered=False,
                    is_paid=False,
                    payment=payment,
                    user=request.user,
                    address=address_details,
                )

                product = cart_item.Product
                product.quantity -= cart_item.quantity
                product.save()
                
            response_data = {'order_id': ordered_product.id,
                             'payment_id': razor_payment['id'],
                             'amount_paid': razor_payment['amount'],
                             'key': settings.KEY,
                             'orders_id':order.id
                             }
          
            return JsonResponse({'response': response_data})
        else:
            cart_items = Cartitem.objects.filter(user=request.user)
            address = request.POST.get('address')
            address_details = Address.objects.get(id=address)

            payment = Payment.objects.create(
                user=request.user,
                payment_method=request.POST.get('paymentmethod'),
                amount=request.POST.get('grandPriceText'),
            )
            payment.save()

            order = Orders.objects.create(
                user=request.user,
                payment=payment,
                address=address_details,
                ordered=False,
                status="New",
                quantity=False,
            )
            order.save()

            for cart_item in cart_items:
                ordered_product = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.Product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.sub_total(),
                    ordered=False,
                    is_paid=False,
                    payment=payment,
                    user=request.user,
                    address=address_details,
                )

                product = cart_item.Product
                product.quantity -= cart_item.quantity
                product.save()
                

            response_data = {'order_id': ordered_product.id,
                             'orders_id':order.id,
                             }
            return JsonResponse({'response': response_data})
    else:
        return JsonResponse({'message': "failed"})

    
    


def orderpage(request):
    orders = Orders.objects.all().order_by("-created_at")
    print(orders)
    return render(request, "admin-templates/page-orders.html", {"orders": orders})




def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
        
            order = Orders.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                pyment=order.payment
                pyment.status='Success'
                pyment.save()


        except Orders.DoesNotExist:
            pass
    return redirect("orderpage")




def order_detail(request,id):
    main_order = Orders.objects.get(pk = id)
    print(main_order)
    orders = OrderProduct.objects.filter(order = main_order)
   
    return render(request,'admin-templates/orders-detail.html',{"orders": orders,"id":id,"main_order":main_order})


def cancel_order(request,id):
    order = Orders.objects.get(pk = id)
    order.status="cancelled"
    order.save()
    return redirect('user_profile')


