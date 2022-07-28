from django.db import models
from crawling.models import Shopinfo
from user.models import User

# Create your models here.

from django.db import models

# Create your models here.
class Review(models.Model):
    id = models.AutoField(auto_created=True, serialize=False,primary_key=True)
    shopId = models.ForeignKey(Shopinfo,on_delete=models.DO_NOTHING)
    userId = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length= 128)
    star = models.IntegerField(default= 0)
