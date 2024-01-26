from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import os
import datetime 



# Create your models here.

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    Password = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    
class Category(models.Model):
    name = models.CharField(max_length=100, null = False, blank = False)
    slug = models.SlugField(max_length=100, null = False, blank = False)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default='')
    slug = models.SlugField(max_length=100, null = False, blank = False, default="unknown")
    img = models.ImageField(upload_to='product', null=True)
    name = models.CharField(max_length=200, unique=True, null=True, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    desc = models.TextField(null=True)
    stock = models.IntegerField(null=True)
    available = models.BooleanField(default=True,blank=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    tag = models.CharField(max_length=150, null=True, blank=True)
    meta_title = models.CharField(max_length=150, null=True, blank=True)
    meta_keywords = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.TextField(max_length=150, null=True, blank=True)
    

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200, null=False)
    lname = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=200, null=False)
    payment_id = models.CharField(max_length=300, null=True)
    orderstatuses = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Completed','completed'),
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='In Progress')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200, null=False)
    lname = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




