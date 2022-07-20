from django.db import models



# Create your models here.

class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    userId = models.CharField(max_length= 128)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length = 128)
    nickname = models.CharField(max_length= 128)
    totalReview = models.IntegerField(default= 0)
    created = models.DateTimeField(auto_now_add=True)
