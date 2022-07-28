from django.db import models

# Create your models here.
class Shopinfo(models.Model):
    id = models.AutoField(auto_created=True, serialize=False,primary_key=True)
    shopName = models.CharField(max_length= 128)
    location = models.CharField(max_length=254)
    phoneNumber = models.CharField(max_length = 128)
    star = models.IntegerField(default= 0)
    comment = models.IntegerField(default= 0)

class Shoppic(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    shopId = models.ForeignKey(Shopinfo,on_delete=models.CASCADE)
    URL = models.TextField()

class Shopmenu(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    shopId = models.ForeignKey(Shopinfo,on_delete=models.CASCADE)
    menu = models.CharField(max_length= 128)
    price = models.CharField(max_length= 128)