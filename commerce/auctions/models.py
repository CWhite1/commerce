from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass


class Listings(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True, related_name="user_listing") 
    category = models.CharField(max_length=64)
    description = models.TextField(default="", max_length=256)
    name =  models.CharField(max_length=64)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField(upload_to='images')
    date = models.DateTimeField(default=now, blank=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)


class Bids(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True, related_name="user_bid") 
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True, related_name="bid_listing")
    bid = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f'Bids {self.id}: {self.listing}: {self.bid}'
        


class Comments(models.Model): 
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_listing")
    comment =  models.CharField(max_length=256)
     
    def __str__(self):
        return self.comment


class Watchlists(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="watchlist")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True, related_name="watchlist")
    
    def __str__(self):
        return str(self.item.id)
