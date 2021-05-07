from django.shortcuts import render
from core.models import Gig


def index(request):
    mostPopulerGigs = Gig.objects.order_by('-quantity')[:3]
    newestGigs = Gig.objects.order_by('-id')[:3]
    context = {
        'title': 'Fiverr Clone',
        'mostPopulerGigs': mostPopulerGigs,
        'newestGigs': newestGigs
    }
    return render(request, 'index.html', context)


def logout(request):
    context = {'title': 'Logout'}
    return render(request, 'logout.html', context)
