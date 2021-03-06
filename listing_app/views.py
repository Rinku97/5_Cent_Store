from django.shortcuts import render
from .models import Listing
from django.core.paginator import Paginator, EmptyPage


# Create your views here.

def listings(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 9)    # to control how pagination works
    page = request.GET.get('page')
    page_listings = paginator.get_page(page)
    context = {
        'listings': page_listings
    }
    return render(request, 'listing_app/listings.html', context)


def listing(request, pk):
    return render(request, 'listing_app/listing.html')


def search(request):
    return render(request, 'listing_app/search.html')
