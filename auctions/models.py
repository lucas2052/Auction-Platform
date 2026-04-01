from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name='users_watchlist')


#定义模型
class category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=14, decimal_places=2)
    image_url = models.URLField()
    category = models.ForeignKey(category, on_delete=models.SET_NULL,blank=True,null=True,related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="won_listings")
    current_highest_bid = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title
    
@property
def current_highest_bid(self):
    highest_bid = self.listing_bids.order_by('-amount').first()
    if highest_bid:
        return highest_bid.amount
    return self.starting_bid


class Bid(models.Model):
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}: {self.content[20]}"



    



    



