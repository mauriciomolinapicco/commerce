from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    imageUrl = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.FloatField()
    imageUrl = models.CharField(null=True, blank=True, max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="listings")
    isActive = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="winner")
    numberOfBids = models.IntegerField()

    def __str__(self):
        return f"{self.user} -> {self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.first_name} for ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    listing = models.ForeignKey(AuctionListing,blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title}-> {self.user} commented: {self.comment}"