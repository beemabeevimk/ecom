

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from adminapp.admin import Product
from products.models import *
# Create your models here.



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

    @property
    def sub_total(self):
        return self.Product.selling_price * self.quantity

    def _str_(self):
        return str(self.Product)
    


    


    
    
    
