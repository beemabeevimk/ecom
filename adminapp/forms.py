from django import forms
# from.models import Amodel
from accounts.models import *
from django.contrib.auth.models import User

from adminapp.models import Brand, Category, Picture, Product


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    #offer = forms.ModelChoiceField(required = False,queryset=Offer.objects.all() ,widget=forms.Select(attrs={'class':'form-select'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile'}),required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)

    class Meta:
        model = Category
        fields = ['name','image', 'description','status']




class BrandForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    model = forms.CharField(required = False, widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)

    class Meta:
        model = Brand
        fields = ['name','model', 'description','status']






class ProductForm(forms.ModelForm):
   
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(),widget=forms.Select(attrs={'class':'form-select'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'name'}))
    product_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile',}),required=False)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'quantity'}))
    selling_price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','id':'selling_price'}))
    original_price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','id':'original_price'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)
    is_available = forms.BooleanField(required=False)
    
    
    class Meta:
        model = Product
        fields = ['category','brand','name', 'product_image', 'quantity','selling_price','original_price', 'description','status',  'is_available']

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = Picture
        fields = ['image']