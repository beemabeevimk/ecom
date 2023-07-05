import datetime
import os
from django.db import models
from django.utils.text import slugify

# Create your models here.


    
def getFileName(request, filename):
        now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
        new_filename = "%s%s"%(now_time, filename)
        return os.path.join('uploads/',new_filename)


# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    # slug = models.SlugField(max_length=100,default='')
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.TextField(max_length=150, null=False, blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name
    
class Product(models.Model):
    
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=100, null=False, blank=False)
    # slug = models.SlugField(max_length=255, null=True, blank=True,default='')
    # vendor = models.CharField(max_length=100, null=False, blank=False)
    product_image = models.ImageField(upload_to='product/',null=False,blank=False,default='')
    quantity = models.PositiveIntegerField(default=0)
    original_price = models.FloatField(null=False,blank=False,default=0)
    selling_price = models.FloatField(null=False,blank=False,default=0)
    offer_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=350, null=False, blank=False,default='')
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending",blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    offer_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    
    
class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_pictures")
    image = models.ImageField(upload_to='product/', blank=True)
    

    def _str_(self):
        return self.image.url
    


class Brand(models.Model):
    name = models.CharField(max_length=100, null= False, blank=False)
    description = models.TextField(max_length=150, null=True, blank=True)
    model = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)          

    def _str_(self):
        return self.name
    


    


    
    


    
