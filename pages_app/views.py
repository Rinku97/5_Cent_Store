from django.shortcuts import render
from listing_app.models import Listing
from listing_app.choices import price_choices, state_choices, category_choices


# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'category_choices': category_choices,
    }
    return render(request, 'pages_app/index.html', context)


def about(request):
    return render(request, 'pages_app/about.html')
