from django.shortcuts import render
from django.http import HttpResponse
from .scrapers import Kkday, Klook


# Create your views here.
# test
# def index(requests):
#     return HttpResponse('Hello World!')

def index(request):

    kkday = Kkday(request.POST.get('city_name'))
    klook = Klook(request.POST.get('city_name'))

    context = {
        "tickets": kkday.scrape() + klook.scrape()
    }

    return render(request, 'tickets/index.html', context)