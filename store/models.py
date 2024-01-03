from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name
    
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.FloatField()
#     digital = models.BooleanField(default=False, blank=True, null=True)

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, blank=True, null=True)
#     transaction_id = models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return str(self.id)

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=0, blank=True, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.product.name
    
# class ShippingOrder(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     state = models.CharField(max_length=200, null=False)
#     zip_code = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address

CharFieldLength = 50

class User(models.Model):
    username = models.CharField(max_length=CharFieldLength)
    password = models.CharField(max_length=CharFieldLength)
    email = models.CharField(max_length=CharFieldLength)
    firstname = models.CharField(max_length=CharFieldLength)
    lastname = models.CharField(max_length=CharFieldLength)

class ShippingAddress(models.Model):
    address = models.CharField(max_length=CharFieldLength)
    city = models.CharField(max_length=CharFieldLength)
    state = models.CharField(max_length=CharFieldLength)
    zip_code = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=CharFieldLength)
    description = models.TextField()
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    brand = models.CharField(max_length=CharFieldLength)

class Category(models.Model):
    name = models.CharField(max_length=CharFieldLength)
    # M-M with Product
    product = models.ManyToManyField(Product) 

class Cart(models.Model):
    # O-O with User  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

class CartItem(models.Model):
    quantity = models.IntegerField()
    # M-O with Cart
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # M-O with Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    # M-O with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # M-O with ShippingAddress (on_delete option to be changed)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    subtotal = models.FloatField()
    # M-O with Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # M-O with Product
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)





