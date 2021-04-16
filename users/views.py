from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib import messages
from gigs.models import Order
from .forms import UserProfileForm


User = get_user_model()


def show(request, id):
    profile = get_object_or_404(User, id=id)
    if request.method == 'PUT':
        if profile == request.user:
            form = UserProfileForm(
                request.PUT, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                user = User.objects.get(id=id)
                user.image.url = user.image.build_url(secure=True)
                user.save()
                messages.success(request, 'Profile Successfully Updated')
            else:
                messages.error(request, "Sorry, Somthing Went Wrong !")
                return redirect('users:edit', profile.id)
        else:
            messages.error(
                request, "Sorry, you don't Have Permission to do that")

    context = {'title': profile, 'profile': profile}
    return render(request, 'users/show.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    profile = get_object_or_404(User, id=id)
    if profile == request.user:
        context = {'title': f'Editing {profile}', 'profile': profile}
        return render(request, 'users/edit.html', context)
    else:
        messages.error(request, "Sorry, You don't Have Perrmission to do that")
        return redirect('users:show', profile.id)


@login_required(login_url='/accounts/google/login/')
def sales(request, id):
    profile = get_object_or_404(User, id=id)
    if profile == request.user:
        if request.method == 'PUT':
            orderId = request.PUT.get('order')
            order = get_object_or_404(Order, id=orderId)
            if order.gig.user == profile:
                order.delivered = request.PUT.get('delivered')
                order.save()
                if request.PUT.get('delivered') == 'True':
                    status = 'Delivered'
                else:
                    status = 'Pending'
                messages.success(request, f"Status Changed to '{status}'")
                return redirect('users:sales', profile.id)
            else:
                messages.error(
                    request, "Sorry, You don't Have Perrmission to do that")
                return redirect('users:sales', profile.id)

        sales = Order.objects.filter(gig__user=id, ordered=True)
        context = {'title': 'My Selles', 'sales': sales}
        return render(request, "users/sales.html", context)
    else:
        messages.error(request, "Sorry, You don't Have Perrmission to do that")
        return redirect('users:show', profile.id)


@login_required(login_url='/accounts/google/login/')
def orders(request, id):
    profile = get_object_or_404(User, id=id)
    if profile == request.user:
        orders = Order.objects.filter(user=profile.id)
        context = {'title': 'My Orders', 'orders': orders}
        return render(request, "users/orders.html", context)
    else:
        messages.error(request, "Sorry, You don't Have Perrmission to do that")
        return redirect('users:show', profile.id)
