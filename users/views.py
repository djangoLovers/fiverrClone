from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib import messages
from gigs.models import Order

from .forms import UserProfileForm

User = get_user_model()

def index(request):
    context = {'title': 'Users'}
    return render(request, 'users/index.html', context)


def show(request, id):
    profile = get_object_or_404(User, id=id)
    if request.method == 'POST':
        if profile.id == request.user.id:
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
    profile = get_object_or_404(User, id=id)
    context = {'title': f'Editing {profile}', 'profile': profile}
    return render(request, 'users/edit.html', context)


@login_required(login_url='/accounts/google/login/')
def my_orders(request):
    user = User.objects.get(id=request.user.id)
    o = Order.objects.filter(gig__user=user, ordered=True)
    print(o)
    return render(request, "users/my_orders.html", {'orders': o})

@login_required(login_url='/accounts/google/login/')
def my_purchases(request):
    my_purchases = Order.objects.filter(user=request.user)
    return render(request, "users/my_purchases.html", {'my_purchases': my_purchases})