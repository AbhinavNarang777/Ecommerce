from django.urls import path
from .import views

urlpatterns=[
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create_Listing", views.create_auction, name='create'),
    path("wishlistt", views.wishlist, name="wish"),
    path("Add/<str:name>", views.add_to_wishlist, name="add_wish"),
    path("Remove/<str:name>", views.rem_from_wishlist, name="rem_wish"),
    path("Active/Products/<str:name>" , views.item,name="item"),
    path("Comment/<str:name>" ,views.comment,name="comment"),
    path("Bid/<str:name>" ,views.Place_Bid,name="bid"),
    path("Close/<str:name>", views.close, name='closed')

]