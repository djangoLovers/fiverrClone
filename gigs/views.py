import requests
from django.contrib import messages
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GigForm
from .models import Category, Gig

# Payment Imports


def index(request):
    gigs = Gig.objects.all()
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def show(request, id):
    gig = get_object_or_404(Gig, id=id)
    if request.method == 'POST':
        if request.user.id == gig.user.id:
            form = GigForm(request.POST, request.FILES, instance=gig)
            if form.is_valid():
                newForm = form.save(commit=False)
                newForm.user = request.user
                newForm.save()
                form.save_m2m()
                messages.success(request, 'Gig Successfully Updated')
            else:
                messages.error(request, 'Somthing Went Wrong ...')
        else:
            messages.error(request, "You Don't have The Permission to do that")
    lastCat = gig.category.all().last()
    context = {'title': gig.name, 'gig': gig, 'lastCat': lastCat}
    return render(request, 'gigs/show.html', context)


@login_required(login_url='/accounts/google/login/')
def new(request):
    form = GigForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.user = request.user
            newForm.save()
            form.save_m2m()
            messages.success(request, 'Gig Successfully Created')
            return redirect(newForm.get_absolute_url())
        else:
            messages.error(request, 'Somthing Went Wrong ..')
    context = {'title': 'New Gig', 'categories': categories, 'form': form}
    return render(request, 'gigs/new.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    gig = get_object_or_404(Gig, id=id)
    if request.user.id == gig.user.id:
        categories = Category.objects.all()
        context = {
            'title': f'Editing {gig.name}',
            'gig': gig, 'categories': categories
        }
        return render(request, 'gigs/edit.html', context)
    else:
        messages.error(request, "You Don't have The Permission to do that")
        return redirect('core:index')


@login_required(login_url='/accounts/google/login/')
def order(request, id):
    gig = get_object_or_404(Gig, id=id)

    if request.method == 'POST':
        data = {
            "merchant_id": "1344b5d4-0048-11e8-94db-005056a205be",
            "amount": round(gig.price) * 24000,
            "callback_url": f"http://127.0.0.1:8000/gigs/{gig.id}/order",
            "description": f"Buying '{gig.name}' Gig"}

        url = "https://api.zarinpal.com/pg/v4/payment/request.json"

        response = requests.post(url, data)
        authority = response.json()['data']['authority']
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')

    status = request.GET.get('Status')
    authority = request.GET.get('Authority')
    context = {'title': 'Payment Callback',
               'status': status, 'authority': authority}
    return render(request, 'gigs/callback.html', context)
