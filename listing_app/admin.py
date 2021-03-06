from django.contrib import admin
from .models import Listing


# To filter out the rpoducts by our ownchoiuce, like by search,category,price,title etc...
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'category', 'price', 'is_published', 'list_date')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'address', 'city', 'zipcode', 'state', 'price')
    list_per_page = 30


admin.site.register(Listing, ListAdmin)
