from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import AuctionListing, User, category
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User


def index(request):
    active_listings = AuctionListing.objects.all()

    user_watchlist = []
    if request.user.is_authenticated:
        user_watchlist = request.user.watchlist.all()

    return render(request, "auctions/index.html" , {
        "listings": active_listings,
        "watchlist": user_watchlist})


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
    
@login_required
def creating_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = float(request.POST["starting_bid"])
        image_url = request.POST["image_url"]
        category_name = request.POST.get("category","")

        category_obj, _ = category.objects.get_or_create(name=category_name)if category_name else(None,False) 
         
        new_listing = AuctionListing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            image_url=image_url,
            category=category_obj,
            owner=request.user,
            is_active=True
        ) 
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")

@login_required
def my_listings(request):
    user_listings = AuctionListing.objects.filter(owner=request.user)
    return render(request, "auctions/my_listings.html", {"listings": user_listings})


def edit_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if listing.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this listing.")
    if request.method =="POST":
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.starting_bid = float(request.POST["starting_bid"])
        listing.image_url = request.POST["image_url"]
        category_name = request.POST.get("category","")
        category_obj, _ = category.objects.get_or_create(name=category_name)if category_name else(None,False) 
        listing.category = category_obj
        listing.save()
        return HttpResponseRedirect(reverse("my_listings"))
    return render(request, "auctions/edit_listing.html", {"listing": listing})


def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    is_watchlisted = False
    if request.user.is_authenticated:
        if listing in request.user.watchlist.all():
            is_watchlisted = True

    return render(request ,"auctions/listing.html", {
        "listing": listing,
        "is_watchlisted": is_watchlisted
        })
            

def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
        messages.success(request, f"{listing.title} has been removed from your watchlist.")
    else:
        request.user.watchlist.add(listing)
        messages.success(request, f"{listing.title} has been added to your watchlist.")

    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))

def watchlist(request):
    items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"listings": items})



