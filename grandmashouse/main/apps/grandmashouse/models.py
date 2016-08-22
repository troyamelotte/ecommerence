from __future__ import unicode_literals
import bcrypt
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    category = models.CharField(max_length=30)
    price = models.FloatField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    address = models.CharField(max_length=200)
    total = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Ordercontent(models.Model):
    product = models.ForeignKey(Product, related_name='OrdercontentToProduct')
    order = models.ForeignKey(Order, related_name= 'OrdercontentToOrder')
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
