from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from core.decorators import isLogged, notLogged
from .forms import UserProfileForm


@isLogged
def index(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Successfully Updated')
            return redirect('users:index')
        return render(request, 'users/edit.html')
    context = {}
    return render(request, 'users/index.html', context)


@isLogged
def edit(request):
    context = {}
    return render(request, 'users/edit.html', context)


@isLogged
def edit(request):
    return render(request, 'users/edit.html')
