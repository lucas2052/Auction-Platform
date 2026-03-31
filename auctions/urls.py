from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.creating_listing, name="create_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listing/<int:listing_id>/edit", views.edit_listing, name="edit_listing"),
    path("toggle_watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("categories", views.category_list, name="category_list"),
    path("category/<str:category_name>", views.category_detail, name="category_detail"),
]
