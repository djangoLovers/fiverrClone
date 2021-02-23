from django.shortcuts import render
from gigs.models import Gig


def index(request):
    gigs = Gig.objects.all().order_by('-id')[:3]
    return render(request, 'index.html', {'title': 'Home Page', 'gigs': gigs})


def logout(request):
    context = {'title': 'Logout'}
    return render(request, 'logout.html', context)
