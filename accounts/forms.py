from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(region="IN",max_length=15, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Code'}))





# from django import forms
# from django.contrib.auth import get_user_model
# from .models import Address

# User = get_user_model()

# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ['user', 'name', 'city', 'pincode', 'phone']

 