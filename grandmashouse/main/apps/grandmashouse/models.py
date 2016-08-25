from __future__ import unicode_literals
import bcrypt
from django.db import models

# Create your models here.

class ProductManager(models.Manager):
    def productcheck(self, name, description,price, category):
        count = 0
        errorlist = []
        if (Product.objects.filter(name=name).count()>0):
            count+=1
            errorlist.append('Name already exists!')
        if len(name)<1:
            count+=1
            errorlist.append('Please print out a valid name')
        if len(description)<20:
            count+=1
            errorlist.append('Please enter a description of over 20 characters!')
        if Category.objects.filter(name=category).count()>0:
            count+=1
            errorlist.append('Category already exists! Select it from the drop down menu.')
        if len(price)<1:
            errorlist.append('Please enter a valid price!')
            count+=1
        if count == 0:
            return True
        return errorlist
    def editcheck(self, name, description,price, category):
        count = 0
        errorlist = []

        if len(name)<1:
            count+=1
            errorlist.append('Please print out a valid name')
        if len(description)<20:
            count+=1
            errorlist.append('Please enter a description of over 20 characters!')
        if Category.objects.filter(name=category).count()>0:
            count+=1
            errorlist.append('Category already exists! Select it from the drop down menu.')
        if len(price)<1:
            errorlist.append('Please enter a valid price!')
            count+=1
        if count == 0:
            return True
        return errorlist

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, related_name='ProductToCategory', default=1)
    price = models.FloatField()
    image = models.ImageField(upload_to = 'photos')
    inventory = models.IntegerField(default = 0)
    sold = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    productManager = ProductManager()
    objects = models.Manager()

class OrderManager(models.Manager):
    def checkorder(self, name, address, city, state, zipcode):
        errorlist = []
        count = 0
        if len(name)<1:
            count+=1
            errorlist.append('Enter a name please!')
        if len(address)<1:
            count+=1
            errorlist.append('Enter a address please!')
        if len(city)<1:
            count+=1
            errorlist.append('Enter a city please!')
        if len(state)<1:
            count+=1
            errorlist.append('Enter a state please!')
        if len(zipcode)<1:
            count+=1
            errorlist.append('Enter a zip code please!')

        if count == 0:
            return True;
        return errorlist


class Order(models.Model):
    name = models.CharField(max_length=100)
    billingname = models.CharField(max_length=100, default=None)
    date = models.DateField()
    address = models.CharField(max_length=200)
    billingaddress = models.CharField(max_length=200, default=None)
    total = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    orderManager = OrderManager()
    objects = models.Manager()


class Ordercontent(models.Model):
    product = models.ForeignKey(Product, related_name='OrdercontentToProduct')
    order = models.ForeignKey(Order, related_name= 'OrdercontentToOrder')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class UserManager(models.Manager):
    def checklog(self, email, password):
        errorlist = []
        count = 0
        if User.objects.filter(email=email).count()<1:
            count+=1
            errorlist.append('Email incorrect')
            return errorlist
        user = User.objects.get(email=email)
        password=password.encode()
        if bcrypt.hashpw(password, user.password.encode()) != user.password:
            count+=1
            errorlist.append('Password incorrect')

        if count == 0:
            return [True, user]
        return errorlist


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()
