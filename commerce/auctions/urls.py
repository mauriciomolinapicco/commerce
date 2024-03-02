from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("placebid", views.placebid, name="placebid"),
    path("removeWatchlist/<str:auctionid>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<str:auctionid>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("displayCategories", views.displayCategories, name="displayCategories"),
    path("category/<str:categoryId>", views.category, name="category"),
    path("comment", views.comment, name="comment"),
    path("finishListing/<str:listingId>", views.finishListing, name="finishListing")
]