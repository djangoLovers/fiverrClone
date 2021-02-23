from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
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
def sales(request, id):
    profile = get_object_or_404(User, id=id)
    if request.user == profile:
        if request.method == 'POST':
            orderId = request.POST.get('order')
            order = get_object_or_404(Order, id=orderId)
            if order.gig.user == profile:
                order.delivered = request.POST.get('delivered')
                order.save()
            else:
                messages.error(
                    request, "Sorry, You don't Have Perrmission to do that")
                return redirect('users:sales', profile.id)

        sales = Order.objects.filter(gig__user=id, ordered=True)
        print(sales)
        context = {'title': 'My Selles', 'sales': sales}
        return render(request, "users/sales.html", context)
    else:
        messages.error(request, "Sorry, You don't Have Perrmission to do that")
        return redirect('users:show', profile.id)


@login_required(login_url='/accounts/google/login/')
def orders(request, id):
    profile = get_object_or_404(User, id=id)
    if request.user == profile:
        orders = Order.objects.filter(user=id)
        context = {'title': 'My Orders', 'orders': orders}
        return render(request, "users/orders.html", context)
    else:
        messages.error(request, "Sorry, You don't Have Perrmission to do that")
        return redirect('users:show', profile.id)
