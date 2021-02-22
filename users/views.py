from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def index(request):
    context = {'title': 'Users'}
    return render(request, 'users/index.html', context)


def show(request, id):
    profile = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        if profile.id == request.id:
            form = UserProfileForm(
                request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Successfully Updated')
            else:
                return render(request, 'users/edit.html', request.user.id)
        else:
            messages.error(
                request, "Sorry, you don't Have Permission to do that")
    context = {'title': profile, 'profile': profile}
    return render(request, 'users/show.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    context = {'title': f'Editing {request.user}'}
    return render(request, 'users/edit.html', context)
