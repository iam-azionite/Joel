from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='products/',null=True,blank=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.product.name

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    address=models.TextField()
    total=models.DecimalField(default=0)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    price=models.DecimalField(default=0,max_digits=10,decimal_places=2)