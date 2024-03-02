from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Category, Comment, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "auctions": AuctionListing.objects.all()
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
    return HttpResponseRedirect(reverse("index") + f"?auctions={AuctionListing.objects.all()}")


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

        return HttpResponseRedirect(reverse("index") + f"auctions={AuctionListing.objects.all()}")
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        imageUrl = request.POST['imageUrl']
        categoryId = request.POST['category']
        category = Category.objects.get(pk=categoryId)

        # Save in the database
        auction = AuctionListing(user=request.user, title=title, description=description, starting_bid=starting_bid, imageUrl=imageUrl, category=category)
        auction.save()

        return render(request, "auctions/index.html",{
            "auctions": AuctionListing.objects.all()
        })

    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html",{
            "categories": categories
        })


def finishListing(request, listingId):
    listing = AuctionListing.objects.get(pk=listingId)
    listing.isActive = False
    bids = listing.bids.all().order_by('amount')
    highestBid = bids.last()
    winner = highestBid.user
    listing.winner = winner
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listingId, )))


def listing(request, id):
    auction = AuctionListing.objects.get(id=id)
    isListingInWatchlist = request.user in auction.watchlist.all()

    return render(request, "auctions/listing.html", {
        "auction": auction,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": Comment.objects.filter(listing=auction),
        "currentBid": auction.bids.all().order_by('amount').last()
    })

        
def addWatchlist(request, auctionid):
    user = request.user
    auction = AuctionListing.objects.get(pk=auctionid)

    auction.watchlist.add(user)

    return HttpResponseRedirect(reverse("listing", args=(auctionid, )))


def removeWatchlist(request, auctionid):
    user = request.user
    auction = AuctionListing.objects.get(pk=auctionid)

    auction.watchlist.remove(user)

    return HttpResponseRedirect(reverse("listing", args=(auctionid, )))


def watchlist(request):
    user = request.user
    auctions = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions
    })


def displayCategories(request):
    categories = Category.objects.all()
    return render(request, "auctions/displayCategories.html", {
        "categories": categories
    })


def category(request, categoryId):
    category = Category.objects.get(pk=categoryId)
    return render(request, "auctions/category.html",{
        "category": category,
        "listings": category.listings.all()
    })


def comment(request):
    if request.method == 'POST':
        content = request.POST["comment"]
        listingid = request.POST["listing"]
        listing = AuctionListing.objects.get(pk=listingid)
        user = request.user
        
        comment = Comment(user=user, comment=content, listing=listing)
        comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listingid, )))


def placebid(request): 
    if request.method == 'POST':
        bid = float(request.POST['bid'])
        listingId = request.POST['id']
        user = request.user
        listing = AuctionListing.objects.get(pk=listingId)

        starting_bid = listing.starting_bid
        bids = listing.bids.all().order_by('amount')
        highestBid = bids.last()

        if bid < starting_bid:
            return render(request, "auctions/listing.html",{
                "auction": listing,
                "message": "The bid must be higher or equal than the starting bid",
                "comments": Comment.objects.filter(listing=listing),
                "currentBid": listing.bids.all().order_by('amount').last()
            })
        else: 
            if highestBid is not None:
                if bid <= highestBid.amount:
                    return render(request, "auctions/listing.html",{
                    "auction": listing,
                    "message": "The bid must be higher than the current bid",
                    "comments": Comment.objects.filter(listing=listing),
                    "currentBid": listing.bids.all().order_by('amount').last()
                    })

        if listing.numberOfBids is None:
            listing.numberOfBids = 1
        else: 
            listing.numberOfBids += 1
        listing.save()
        
        newBid = Bid(user=user, amount=bid, listing=listing)
        newBid.save()
        return render(request, "auctions/listing.html",{
                "auction": listing,
                "message": "Bid succesfully placed!!",
                "comments": Comment.objects.filter(listing=listing),
                "currentBid": listing.bids.all().order_by('amount').last()
            })


