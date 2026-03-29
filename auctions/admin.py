from django.contrib import admin
from .models import User, category, AuctionListing

admin.site.register(User)
admin.site.register(category)
admin.site.register(AuctionListing)


# Register your models here.
