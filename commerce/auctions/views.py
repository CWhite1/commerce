from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from decimal import Decimal

from .models import User, Listings, Bids, Comments, Watchlists
from .forms import Item, Bid, Comment


def index(request):
    """Process item uploaded by users"""
    all_listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : all_listings
        })

def active(request):
    """Process item uploaded by users"""
    # Get all active listings (where the `is_active` field is True)
    active_listings = Listings.objects.filter(active=True)
    return render(request, "auctions/active.html", {
        "listings" : active_listings
        })


def create(request):
    """Process item uploaded by users"""
    form = Item(request.POST, request.FILES)
    if request.method == 'POST':    
        if form.is_valid():
            original = form.save(commit=False)
            original.author = request.user
            original.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, "auctions/create.html", {
                'form': form, 'img_obj': img_obj
                })
    else:
        form = Item()       
    return render(request, 'auctions/create.html', {'form': form})
   

def list(request, listing_id):
    """Process to View Listing"""
    # Accessing the data for item in Listings Model
    item = Listings.objects.get(pk=listing_id)
    comments = Comments.objects.filter(listing=item)
    # Create variable for template to determine which watchlist button/form is displayed
    item_exists = Watchlists.objects.filter(user=request.user, item=item).exists()
    # Determine if user is the author of listing
    author = Listings.objects.filter(pk=listing_id, author=request.user).exists()
    # Determine if current user is the winner of the current listings bid.
    winner = Listings.objects.filter(pk=listing_id, winner=request.user).exists()
    # Determine if user is the author of listing
    author = Listings.objects.filter(pk=listing_id, author=request.user).exists()
    # get all comments for current List''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Create empty forms for template
    form_b = Bid()   
    form_c = Comment()
    # Display Listing, Empty Forms, Watchlist Buttons or if winner or author of listing on template
    return render(request, 'auctions/listing.html', {
        'form_b': form_b,
        'form_c': form_c, 
        'listing': item,
        'item_exists': item_exists,
        "author": author,
        "winner": winner,
        "comments": comments
        })


def categories(request):
    # Get a list of all the unique values in the category field
    categories = Listings.objects.values_list('category', flat=True).distinct()

    # Filter the Listings queryset to only include objects where the category field is equal to one of the values in the categories list
    listings = Listings.objects.filter(category__in=categories)
    return render(request, "auctions/categories.html", {                        
                        "categories" : categories,
                        }) 


def category_page(request, category):
    listings = Listings.objects.filter(category=category)
    return render(request, 'auctions/category_page.html', {'listings': listings})


@login_required
def close(request, listing_id):
    # Identify Current Listing
    item = Listings.objects.get(pk=listing_id)
    # Retrieve all the bids for the listing from the database
    bids = Bids.objects.filter(listing=item)
    # Identify Highest Bid for Listing or assign Value of 0
    bid = Bids.objects.filter(listing=listing_id).aggregate(Max('bid'))['bid__max']
    # if close button clicked
    if request.method == 'POST':
        # if no bids, display response
        if bid is None:
            return render(request, "auctions/listing.html", {
                'listing': item, 
                "message": "No Bids Have been Made"
                })
        else:
            # Find the highest bid
            highest_bid = max(bids, key=lambda bid: bid.bid)
            # Identify the author of the highest bid
            bid_winner = highest_bid.author
            # create winner of Listing
            item.winner = bid_winner.username
            # mark listing as inactive
            item.active = False
            # save into db listing no longer active / closed
            item.save()
            # render listings template with message
            return render(request, "auctions/listing.html", 
            {'listing': item, 
            "message": "Bid Approved, This Listing is Now Closed"
            })
                

def comment(request, listing_id):
    item = Listings.objects.get(pk=listing_id)
    form_c = Comment(request.POST, request.FILES) 
    # Create variable for template to determine which watchlist button/form is displayed
    item_exists = Watchlists.objects.filter(user=request.user, item=item).exists()
    if request.method == 'POST':
        # check if comment form is valid
        if form_c.is_valid():
            # save comment into variable original
            new_comment = form_c.save(commit=False)
            # assign listing associated with comment
            new_comment.listing = item
            # save comment and listing that it is associated with
            new_comment.save()
            # Get the current comment to display in the template
            comment =  form_c.instance 
            return render(request, "auctions/listing.html", { 
                'comment': comment, 
                "item_exists": item_exists, 
                'listing': item,
                })
    


@login_required
def bid(request, listing_id):
    # Identify current listing passed through form actions listing.id
    item = Listings.objects.get(pk=listing_id)
    # Identify Highest Bid for Listing or assign Value of 0
    highest_bid = Bids.objects.filter(listing=listing_id).aggregate(Max('bid'))['bid__max']  or Decimal('0')
    # field for Watchlist Add or Remove
    item_exists = Watchlists.objects.filter(user=request.user, item=item).exists()
    # Identify Bid form
    form_b = Bid(request.POST, request.FILES)
    if request.method == 'POST':
        # if request method is Post and form is valid
        if form_b.is_valid():
                # Get input user submitted
                query = request.POST.get('bid')
                # Identify starting price and turn into int
                s_price = float(item.price)
                # give query an integer value
                query = float(query)
                # give highest bid for listing an integer value
                highest_bid = float(highest_bid)
                # if users input is larger than starting price and highest bid 
                if query >= s_price and query > highest_bid:
                    # save bid from form into variable original
                    original = form_b.save(commit=False)
                    # assign author of bid
                    original.author = request.user
                    # assign listing associated with bid
                    original.listing = item 
                    # save bid to listing and current author
                    original.save()
                    # Get the current bid to display in the template
                    bid =  form_b.instance
                    return render(request, "auctions/listing.html", {'bid': bid, "item_exists": item_exists, 'listing': item, })
                elif query < s_price and s_price > highest_bid: 
                    # if query less than starting price is highest submit error
                    return render(request, "auctions/error.html", {                    
                        "s_price": s_price
                        }) 
                else:
                    # if bid not greater than highest bid but greater than starting price submit error 
                    return render(request, "auctions/error.html", {                        
                        "highest_bid" : highest_bid,
                        }) 

                    
@login_required
def watchlist(request):
    # Get current user
    user = request.user
    # Get current users listings from Watchlist
    listings = Watchlists.objects.filter(user=user)
    # Display users watchlist linsting on Template
    return render(request, 'auctions/watchlist.html', {
        "listings" : listings,    
        })


@login_required
def watchlist_add(request, listing_id):
    # Identtify item from listing table
    item = Listings.objects.get(pk=listing_id)
    if request.method == "POST":
        # Insert item and current user into Watchlist table
        Watchlists.objects.create(user=request.user, item=item)
        # Redirect user to listing
        return HttpResponseRedirect(reverse("listing", args=(item.id,)))    


@login_required
def watchlist_remove(request, listing_id): 
    # Identtify item from Listings table
    item = Listings.objects.get(pk=listing_id)
    # Identify Watchlists row for current listing into assign into a variable
    listing =  Watchlists.objects.filter(user=request.user, item=item)
    if request.method == "POST":   
        #Delete Row from Watchlists table  
        listing.delete()
        # Redirect user to listing
        return HttpResponseRedirect(reverse("listing", args=(item.id,)))

                   
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
