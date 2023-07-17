
# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from adminapp.admin import Product
from products.models import *
# Create your models here.

from accounts.models import * 
from ecom import settings
from django.conf import settings

User=get_user_model()

# Create your models here.
class   Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return str(self.user)


class Cartitem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)  
    Product = models.ForeignKey(Product,on_delete=models.CASCADE )
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    total=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    

    # @property  
    def sub_total(self):
        return self.Product.selling_price * self.quantity

    def _str_(self):
        return str(self.Product)
    


    





# order tables


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("Razorpay", "Razorpay"),
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cash")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    status = models.CharField(max_length=100,default="")

    def __str__(self):
        return f"{self.payment_method} - {self.amount}"





class Orders(models.Model):
    STATUS = (
        ("confirmed","confirmed"),
        ("pending","pending"),
        ("shipped","shipped"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
    )
    
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.CASCADE,max_length=255)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=STATUS ,default="New")
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ["-ordered"]

    def __str__(self):
        return f"Order {self.id} by {self.user}"





class OrderProduct(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_products")
    address = models.ForeignKey(Address,on_delete=models.CASCADE,default=0)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="pending")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="order_products" )
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name="order_products")

    def __str__(self):
        return f"{self.product} - {self.quantity}"



   

    
    
    
