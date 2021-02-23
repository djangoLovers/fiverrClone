from django.shortcuts import render
from gigs.models import Gig


def index(request):
    mostPopulerGigs = Gig.objects.all().order_by('-orderedTime')[:3]
    newestGigs = Gig.objects.all().order_by('-id')[:3]
    context = {
        'title': 'Home Page',
        'mostPopulerGigs': mostPopulerGigs,
        'newestGigs': newestGigs
    }
    return render(request, 'index.html', context)


def logout(request):
    context = {'title': 'Logout'}
    return render(request, 'logout.html', context)
