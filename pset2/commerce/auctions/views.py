from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms # Needed for django built-in forms
from django.contrib.auth.decorators import login_required # Adding for login only views

from .models import User, Auction, Comment, Bid

# Default URL if user does not enter image URL
DEFAULT_URL = 'https://online-learning.harvard.edu/sites/default/files/styles/social_share/public/course/cs50x-original.jpg?itok=kR_JV8DW'

# Form to create a new auction
class NewAuctionForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    description = forms.CharField(widget=forms.Textarea(), label="Description")
    starting_bid = forms.DecimalField(max_digits=50, label="Starting Price")
    image_url = forms.URLField(required=False, label="Image URL")
    category = forms.CharField(max_length=100, widget=forms.Select(choices=Auction.CATEGORY_CHOICES), label="Category")

# Form to post a comment
class NewCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="Content")

# Form to bid on an item
class NewBidForm(forms.Form):
    bid = forms.DecimalField(max_digits=50, label="Bid")

def index(request):
    return render(request, "auctions/index.html", {
        "header": "Active Listings",
        "auctions": Auction.objects.filter(active=True).order_by('-timestamp')
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def create(request):
    # If post, save to DB and redirect to the main page
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewAuctionForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]

            # Check if user as provided an image URL
            if (form.cleaned_data["image_url"]):
                image_url = form.cleaned_data["image_url"]
            else: # If not, use a default image
                image_url = DEFAULT_URL

            category = form.cleaned_data["category"]
            current_user = request.user

            # When creating, highest_bid=starting_bid
            highest_bid=starting_bid

            # Write to DB, Auction table
            auction = Auction(creator=current_user, title=title, description=description, starting_bid=starting_bid, highest_bid=highest_bid, image_url=image_url, category=category)
            auction.save()

        return HttpResponseRedirect(reverse("index"))
    # Else, display the create page
    else:
        return render(request, "auctions/create.html", {
        "form": NewAuctionForm()
    })


def auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)

    # Extract the highest bid and winner, if it exists, else return starting price.
    try:
        Bid.objects.filter(auction=auction).get(bid=auction.highest_bid)
    except:
        highestbid = auction.highest_bid
        highestbidder = auction.creator
    else:
        highestbid = Bid.objects.filter(auction=auction).get(bid=auction.highest_bid)
        highestbidder = highestbid.bidder

    # If user is authenciated allow to add/remove to/from watch list
    if request.user.is_authenticated:
        # Check if item is in user's watchlist
        in_watchlist = Auction.objects.filter(id=auction_id).filter(watchers=request.user)

        # Extra later to determine if the user is the author, allow to close the auction.
        if request.user == auction.creator:
            user_is_owner = 1
        else:
            user_is_owner = 0

        # Check if the user is the highest bidder and if the auction is closed
        if request.user == highestbidder and not (Auction.objects.get(id=auction_id).active):
            user_is_winner = 1
        else:
            user_is_winner = 0
    else:
        in_watchlist = 0
        user_is_owner = 0
        user_is_winner = 0

    comments = Comment.objects.filter(auction=auction)
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "NewCommentForm": NewCommentForm,
        "NewBidForm": NewBidForm,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "user_is_owner": user_is_owner,
        "user_is_winner": user_is_winner
    })

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def add_comment(request, auction_id):
    # Take in the data the user submitted and save it as form
    form = NewCommentForm(request.POST)

    # Check if form data is valid (server-side)
    if form.is_valid():

        # Isolate the items from the 'cleaned' version of form data
        auction = Auction.objects.get(id=auction_id)
        content = form.cleaned_data["content"]

        # Get user ID, from https://docs.djangoproject.com/en/1.7/topics/auth/default/#authentication-in-web-requests
        current_user = request.user

        # Write to DB, comment table
        comment = Comment(author=current_user, content=content, auction=auction)
        comment.save()

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def bid(request, auction_id):
    # Take in the data the user submitted and save it as form
    form = NewBidForm(request.POST)
    # Check if form data is valid (server-side)
    if form.is_valid():

        # Isolate the items from the 'cleaned' version of form data
        auction = Auction.objects.get(id=auction_id)
        amount = form.cleaned_data["bid"]
        current = auction.highest_bid

        # Get user ID, from https://docs.djangoproject.com/en/1.7/topics/auth/default/#authentication-in-web-requests
        current_user = request.user

        if (amount > current):
            # Write to Bid DB
            bid = Bid(bidder=current_user, auction=auction, bid=amount)
            bid.save()

            # also Update the current price of the item in the auction DB
            auction.highest_bid = amount
            auction.save()
        else:
            return render(request, "auctions/error.html", {
                "message": "New bid must be higher than the current price."
            })
    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def add_rem_watchlist(request, auction_id):

    # Get user ID, from https://docs.djangoproject.com/en/1.7/topics/auth/default/#authentication-in-web-requests
    current_user = request.user
    auction = Auction.objects.get(id=auction_id)

    in_watchlist = Auction.objects.filter(id=auction_id).filter(watchers=current_user)

    if in_watchlist:
        auction.watchers.remove(current_user)
    else:
        auction.watchers.add(current_user)

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def watchlist(request):
    # Get user ID, from https://docs.djangoproject.com/en/1.7/topics/auth/default/#authentication-in-web-requests
    current_user = request.user

    watchlist = Auction.objects.filter(watchers=current_user)
    return render(request, "auctions/index.html", {
        "header": "Watchlist",
        "auctions": watchlist
    })

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def close(request, auction_id):
    # Isolate the items from the 'cleaned' version of form data
    auction = Auction.objects.get(id=auction_id)

    # Get user ID, from https://docs.djangoproject.com/en/1.7/topics/auth/default/#authentication-in-web-requests
    current_user = request.user

    if current_user == auction.creator:
            auction.active = 0
            auction.save()

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

def categories(request):
    categories = Auction.CATEGORY_CHOICES
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(active=True).filter(category=category).order_by('-timestamp')
    })
