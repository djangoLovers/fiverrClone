from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .forms import UserProfileForm


def index(request):
    context = {'title': 'Users'}
    return render(request, 'users/index.html', context)


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


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    context = {'title': f'Editing {request.user}'}
    return render(request, 'users/edit.html', context)
