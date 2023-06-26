from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField 
from accounts.manager import CustomUserManager

# from django.contib.auth.models import user 
# Create your models here.


class CustomUser(AbstractUser):
    username = None
    name=models.CharField(max_length=50,default=None)
    phone_number = PhoneNumberField(max_length=15, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=255, unique=True)
    password=models.CharField(max_length=100)
    is_verified = models.BooleanField(default= True)                                        
    is_active = models.BooleanField(default= True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    objects = CustomUserManager()
    

class profile(models.Model):
    # user = models.OneToOneField(user, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

