from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})


def logout(request):
    context = {'title': 'Logout'}
    return render(request, 'logout.html', context)
