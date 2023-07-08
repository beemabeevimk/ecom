from django.db import models

from accounts.models import User
from django.contrib.auth import get_user_model
from adminapp.admin import Product
from accounts.models import Address
# from adminapp.admin import Address,Payment,ProductVariant
# Create your models here.


class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('out for shipping','out for shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
       )

    user    = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null= True) 
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=50,null=True)
    order_note = models.CharField(max_length=50, blank=True)
    order_total = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=50,choices=STATUS,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.address.name)

    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="myorders")
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variation = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, null=True) 
    quantity = models.IntegerField()
    product_price = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return f"{self.user}-{self.product} - {self.quantity}"


User = get_user_model()

class Payment(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.name}--{self.payment_method}"



