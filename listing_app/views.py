from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, EmptyPage
from .choices import price_choices, state_choices, category_choices

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
    listing = get_object_or_404(Listing, pk=pk)
    context = {
        'listing': listing
    }
    return render(request, 'listing_app/listing.html', context)


def search(request):
    query_set = Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_set = query_set.filter(description__icontains=keywords)
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set = query_set.filter(city__iexact=city)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            query_set = query_set.filter(category__iexact=category)
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_set = query_set.filter(state__iexact=state)
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)
    context = {
        'query_set': query_set,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'category_choices': category_choices,
        'values': request.GET,
    }
    return render(request, 'listing_app/search.html', context)
