from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from itertools import product
from time import time
from xmlrpc.client import DateTime
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime 

# create models for what all things we need in our website

# user model
class User(AbstractUser):
    pass

# item model
class Item(models.Model):
    title= models.CharField(max_length=50)
    description= models.TextField(blank=True)
    seller= models.ForeignKey(User, on_delete=models.CASCADE)
    time= models.DateTimeField(default=datetime.now)
    photo= models.ImageField(default="images/noimage.jpg",upload_to='images')
    closed= models.BooleanField(default=False)

    # default declaraton/display
    def __str__(self):
        return f"{self.title}, {self.closed}"


# wishlist for customer
class Wishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Item, on_delete=models.CASCADE)


# comments for certain product
class Comments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Item, on_delete=models.CASCADE)
    comment= models.TextField(max_length=1000)

# actual bid for a product
class Bid(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Item, on_delete=models.CASCADE)
    bid_amount= models.IntegerField()

    # displaying the bid
    def __str__(self):
        return f"{self.user} placed {self.bid_amount} on {self.product}"
