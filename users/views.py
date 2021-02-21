from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from core.decorators import isLogged, notLogged
from .forms import UserProfileForm


@isLogged
def index(request):
    context = {'title': 'Users'}
    return render(request, 'users/index.html', context)


@isLogged
def show(request, id):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Successfully Updated')
        else:
            return render(request, 'users/edit.html', request.user.id)
    context = {'title': request.user}
    return render(request, 'users/show.html', context)


@isLogged
def edit(request, id):
    context = {'title': f'Editing {request.user}'}
    return render(request, 'users/edit.html', context)
