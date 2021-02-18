from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})
