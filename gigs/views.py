import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GigForm, CommentForm
from .models import Category, Comment, Gig, Order


def search(request):
    query = request.GET.get('q')
    count = 0
    if query is not None:
        gigs_result = Gig.objects.search(query)
        count = len(gigs_result)
    return render(request, 'gigs/search.html',
                  {'results': gigs_result, 'count': count, 'query': query})


def index(request):
    gigs = Gig.objects.all()
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def show(request, id):
    gig = get_object_or_404(Gig, id=id)
    orderedCheck = Order.objects.filter(
        user=request.user.id, gig=gig, ordered=True)
    if len(orderedCheck):
        res = True
    else:
        res = False

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
    context = {'title': gig.name, 'gig': gig,
               'lastCat': lastCat, 'ordered': res}
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
def comment(request, id):
    gig = get_object_or_404(Gig, id=id)
    if request.method == 'POST':
        orderedCheck = Order.objects.filter(
            user=request.user, gig=gig).exists()

        if orderedCheck:
            form = CommentForm(request.POST)
            if form.is_valid():
                newForm = form.save(commit=False)
                newForm.gig = gig
                newForm.user = request.user
                newForm.save()
                messages.success(request, 'Thanks For Your Review !')
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
        merchant_id = '1344b5d4-0048-11e8-94db-005056a205be'
        amount = round(gig.price) * 24000
        data = {
            "merchant_id": merchant_id,
            "amount": amount,
            "callback_url": 'http://127.0.0.1:8000/gigs/callback',
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
    merchant_id = '1344b5d4-0048-11e8-94db-005056a205be'
    order = request.user.orders_user.last()
    amount = round(order.gig.price) * 24000
    status = request.GET.get('Status')
    authority = request.GET.get('Authority')
    data = {
        'merchant_id': merchant_id,
        'amount': amount,
        'authority': authority}

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
