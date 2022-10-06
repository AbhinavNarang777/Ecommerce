from django.http import HttpResponse, HttpResponseRedirect
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from .models import Comments, User, Item, Wishlist, Bid
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# create views to load related templates

def index(request):
    items= Item.objects.filter(closed=False).order_by('-time').all()
    # which template to render
    return render(request, "auctions/index.html",{
        'items':items

    })

def login_view(request):
    if request.method=="POST":

        # attempt to sign in
        username= request.POST["username"]
        password = request.POST["password"]
        user= authenticate(request, username=username, password =password)

        # check if authenticated successfully
        if user is not None:
            login(request, user)
            return HTTPResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HTTPResponseRedirect(reverse("index"))


def register(request):
    if request.method=="POST":
        username = request.POST["username"]
        email= request.POST["email"]

        # PASSWORD VERIFICATION
        password= request.POST["password"]
        confirmation= request.POST["confirmation"]
        if password!=confirmation:
            return render(request, "auctions/register.html" ,{
                "message": "Password must match."
            })

        # Attemt to create new user
        try:
            user = User.ojects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "aurctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HTTPResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required()
def create_auction(request):
    if request.method=="POST":
        item= Item()
        item.title= request.POST['title']
        item.description= request.POST['description']
        item.photo= request.POST['image']
        if item.photo in request.POST:
            item.photo= request.FILES['image']
        item.start_price= request.POST['price']
        item.seller= request.user
        item.save()
        return redirect('item', name= item.title)
    else:
        return render(request, "auctions/create_auction.html")

#view to be rendered when we click on an item
def item(request, name):
    item= Item.objects.filter(title=name).first()
    comments= Comments.objects.filter(product=item).all()
    bid= Bid.objects.filter(product=item).order_by('-bid_amount').first()
    bid_count= len(Bid.objects.filter(product=item).all())
    if item.closed==False:
        if request.user.is_anonymous:
            return render(request, "auction/item.html", {
                'item': item,
                'comments': comments,
                'bid': bid,
                'bid_count': bid_count
            })
        
        else:
            if request.user== item.seller:
                option_for_close= True
            else:
                option_for_close= False
            wishlist= Wishlist.objects.filter(user= request.user, product= item)
            if wishlist:
                return render(request, "auctions\item.html", {
                    "item": item,
                    'added' : 'the product is already in wishlist',
                    'comments': 'comments',
                    'bid': bid,
                    'bid_count': bid_count,
                    'option_for_close': option_for_close
                })
            else:
                return render(request, "auctions\item.html", {
                    "item":item,
                    'absent':'the product is not in the wishlist',
                    'comments':comments,
                    'bid':bid,
                    'bid_count':bid_count,
                    'option_for_close':option_for_close
                })
    else:
        return render(request, "auctions\item.html", {
            'item': item,
            'commnts': comments,
            'bid': bid,
            'bid_count': bid_count,
            'closed': True
        })

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user = request.user)
    return render(request,"auctions/wishlist.html",{
        'items':items
    })

@login_required
def add_to_wishlist(request,name):
    item = Item.objects.filter(title=name).first()
    bid = Bid.objects.filter(product=item).order_by('-bid_amount').first()
    bid_count = len(Bid.objects.filter(product=item).all())
    add_to_wish = Wishlist()
    add_to_wish.user = request.user
    add_to_wish.product = item 
    add_to_wish.save()
    return render(request,"auctions/item.html",{
        'item':item,
        'added':'the product is already in wishlist',
        "message_added":"Added to wishlist",
        'bid':bid,
        'bid_count':bid_count
    })

@login_required
def rem_from_wishlist(request,name):
    item = Item.objects.filter(title=name).first()
    bid = Bid.objects.filter(product=item).order_by('-bid_amount').first()
    bid_count = len(Bid.objects.filter(product=item).all())
    wishlist = Wishlist.objects.filter(user=request.user, product=item)
    wishlist.delete()
    return render(request,"auctions/item.html",{
        'item':item,
        'absent':'the product is not in the wishlist',
        "message_removed":"Removed From wishlist",
        'bid':bid,
        'bid_count':bid_count
    })

@login_required()
def comment(request,name):
    item = Item.objects.filter(title=name).first()
    if request.method == "POST":
        new_comment = Comments()
        new_comment.user = request.user
        new_comment.product = item
        new_comment.comment= request.POST['comment']
        new_comment.save()
        return redirect('item',name = name)
    else:
        return render(request,'auctions/item.html')

@login_required()
def Place_Bid(request,name):
    item = Item.objects.filter(title=name).first()
    if request.method=='POST':
        bid = Bid()
        bid.user = request.user
        bid.product = item
        bid.bid_amount = request.POST['bid']
        bid.save()
        return redirect('item',name = name)
    else:
        return render(request,'auctions/item.html')

@login_required(login_url=login)
def close(request,name):
    item = Item.objects.filter(title=name).first()
    item.closed = True
    item.save()
    return redirect('item', name=name) 