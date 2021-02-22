from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from gigs.models import Order
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import UserProfileForm

User = get_user_model()

def index(request):
    context = {'title': 'Users'}
    return render(request, 'users/index.html', context)


def show(request, id):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user)
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


@login_required(login_url='/accounts/google/login/')
def my_orders(request):
    user = User.objects.get(id=request.user.id)
    o = Order.objects.filter(gig__user=user, ordered=True)

    return render(request, "users/my_orders.html", {'orders': o})

@login_required(login_url='/accounts/google/login/')
def my_purchases(request):
    my_purchases = Order.objects.filter(user=request.user)
    print(my_purchases)

    return render(request, "users/my_purchases.html", {'my_purchases': my_purchases})