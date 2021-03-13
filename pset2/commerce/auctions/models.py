from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):

    # Default URL if user does not enter image URL
    DEFAULT_URL = 'https://online-learning.harvard.edu/sites/default/files/styles/social_share/public/course/cs50x-original.jpg?itok=kR_JV8DW'
    # From amazon.com
    CATEGORY_CHOICES = [
        ('BABY', 'Baby'),
        ('BEAUTY', 'Beauty'),
        ('BOOKS', 'Books'),
        ('CAMERA_PHOTO', 'Camera & Photo'),
        ('CLOTHING_ACCESSORIES', 'Clothing & Accessories'),
        ('CONSUMER_ELECTRONICS', 'Consumer Electronics'),
        ('GROCERY_GOURMET_FOODS', 'Grocery & Gourmet Foods'),
        ('HEALTH_PERSONAL_CARE', 'Health & Personal Care'),
        ('HOME_GARDEN', 'Home & Garden'),
        ('INDUSTRIAL_SCIENTIFIC', 'Industrial & Scientific'),
        ('LUGGAGE_TRAVEL_ACCESSORIES', 'Luggage & Travel Accessories'),
        ('MUSICAL_INSTRUMENTS', 'Musical Instruments'),
        ('OFFICE_PRODUCTS', 'Office Products'),
        ('OUTDOORS', 'Outdoors'),
        ('PERSONAL_COMPUTERS', 'Personal Computers'),
        ('PET_SUPPLIES', 'Pet Supplies'),
        ('SHOES_ANDBAGS_SUNGLASSES', 'Shoes, Handbags, & Sunglasses'),
        ('SOFTWARE', 'Software'),
        ('SPORTS', 'Sports'),
        ('TOOLS_HOME_IMPROVEMENT', 'Tools & Home Improvement'),
        ('TOYS', 'Toys'),
        ('VIDEOGAMES', 'Video Games'),
        ('OTHER', 'Other')
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(default="0.00", decimal_places=2, max_digits=50)
    highest_bid =  models.DecimalField(default="0.00", decimal_places=2, max_digits=50)
    image_url = models.URLField(blank=True, null=True, default=DEFAULT_URL)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders", null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction", null=True)
    bid = models.DecimalField(decimal_places=2, max_digits=50, default="0.00")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.bidder} bid {self.bid} on {self.auction} at {self.timestamp}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.author} commented at {self.timestamp}: {self.content}"
