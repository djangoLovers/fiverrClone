import requests
from os import environ
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GigForm, CommentForm
from .models import Category, Comment, Gig, Order
from .filter import gigFilter


def index(request):
    gigs = Gig.objects.all()
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.user = request.user
            newForm.save()
            form.save_m2m()
            messages.success(request, 'Gig Successfully Created')
            return redirect('gigs:show', newForm.id)
        else:
            messages.error(request, 'Somthing Went Wrong ..')
            return redirect('gigs:new')
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def search(request):
    categories = Category.objects.all()
    query = {
        'q': request.GET.get('q'),
        'category': request.GET.get('category')
    }
    gigs_result = Gig.objects.search(query['q'])
    filter = gigFilter(request.GET, queryset=gigs_result)
    gigs_result = filter.qs
    count = gigs_result.count()
    context = {
        'title': 'Search Result',
        'results': gigs_result,
        'count': count,
        'query': query,
        'filter': filter,
        'categories': categories
    }
    return render(request, 'gigs/search.html', context)


def show(request, id):
    gig = get_object_or_404(Gig, id=id)
    try:
        orderedCheck = Order.objects.filter(
            user=request.user, gig=gig, ordered=True).exists()
    except:
        orderedCheck = False
    if request.method == 'PUT':
        if request.user.id == gig.user.id:
            form = GigForm(request.PUT, request.FILES, instance=gig)
            if form.is_valid():
                newForm = form.save(commit=False)
                newForm.user = gig.user
                newForm.save()
                form.save_m2m()
                messages.success(request, 'Gig Successfully Updated')
            else:
                messages.error(request, 'Somthing Went Wrong ...')
        else:
            messages.error(request, "You Don't have The Permission to do that")

    context = {'title': gig.name, 'gig': gig, 'ordered': orderedCheck}
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
            return redirect('gigs:show', newForm.id)
        else:
            messages.error(request, 'Somthing Went Wrong ..')
    context = {'title': 'New Gig', 'categories': categories, 'form': form}
    return render(request, 'gigs/new.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    gig = get_object_or_404(Gig, id=id)
    if request.user == gig.user:
        categories = Category.objects.all()
        context = {
            'title': f'Editing {gig.name}',
            'gig': gig,
            'categories': categories
        }
        return render(request, 'gigs/edit.html', context)
    else:
        messages.error(
            request, "Sorry, You Don't have The Permission to do that")
        return redirect('gigs:show', gig.id)


@login_required(login_url='/accounts/google/login/')
def comment(request, id):
    gig = get_object_or_404(Gig, id=id)
    orderedCheck = Order.objects.filter(
        user=request.user, gig=gig, ordered=True).exists()

    if orderedCheck:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                if int(request.POST['rating']) in range(1, 6):
                    newForm = form.save(commit=False)
                    newForm.gig = gig
                    newForm.user = request.user
                    newForm.save()
                    messages.success(request, 'Thanks For Your Review !')
                else:
                    messages.error(request, 'Please Set a Valid Rating !')
            else:
                messages.error(request, 'Somhting Went Wrong, Try Again !')

        if request.method == 'DELETE':
            commentId = request.DELETE.get('id')
            comment = get_object_or_404(Comment, id=commentId)
            if comment.user == request.user:
                comment.delete()
                messages.success(request, 'Comment Successfuly Deleted !')
    else:
        messages.error(
            request, "Sorry, you don't Have Permission to do that")
    return redirect('gigs:show', id)


@login_required(login_url='/accounts/google/login/')
def order(request, id):

    if request.method == 'POST':
        gig = get_object_or_404(Gig, id=id)
        merchant_id = environ.get('MERCHANT_ID')
        amount = round(gig.price) * 24000
        data = {
            "merchant_id": merchant_id,
            "amount": amount,
            "callback_url": 'https://fiverr-clone.herokuapp.com/gigs/callback',
            "description": f"Buying '{gig.name}' Gig"
        }

        response = requests.post(
            "https://api.zarinpal.com/pg/v4/payment/request.json", data)
        authority = response.json()['data']['authority']

        o = Order(user=request.user, gig=gig, ordered=False, delivered=False)
        o.save()

        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return redirect('gigs:show', id)


def callback(request):
    merchant_id = environ.get('MERCHANT_ID')
    order = request.user.orders_user.last()
    amount = round(order.gig.price) * 24000
    status = request.GET.get('Status')
    authority = request.GET.get('Authority')
    data = {
        'merchant_id': merchant_id,
        'amount': amount,
        'authority': authority
    }

    if status == 'NOK':
        response = requests.post(
            'https://api.zarinpal.com/pg/v4/payment/verify.json', data)

        gig = Gig.objects.get(id=order.gig.id)
        gig.quantity += 1
        gig.save()
        order.ordered = True
        order.save()

    request.session['status'] = status
    request.session['authority'] = authority
    return redirect('gigs:result')


def result(request):
    try:
        status = request.session['status']
        authority = request.session['authority']

        del request.session['status']
        del request.session['authority']

        context = {
            'title': 'Payment Result',
            'authority': authority,
            'status': status
        }
        return render(request, 'gigs/result.html', context)
    except:
        return redirect('core:index')
