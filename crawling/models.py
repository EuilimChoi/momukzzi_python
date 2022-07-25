from os import PRIO_PROCESS
from unicodedata import category
from django.db import models

# Create your models here.
class Shopinfo(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    shopId = models.CharField(max_length= 128)
    shopName = models.CharField(max_length= 128)
    location = models.CharField(max_length=254)
    phoneNumber = models.CharField(max_length = 128)
    star = models.IntegerField(default= 0)
    comment = models.IntegerField(default= 0)

class Shoppic(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    shopId = models.CharField(max_length= 128)
    URL = models.TextField()

class Shopmenu(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    shopId = models.CharField(max_length= 128)
    menu = models.CharField(max_length= 128)
    price = models.CharField(max_length= 128)