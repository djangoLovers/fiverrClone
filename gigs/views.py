from typing import Match
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GigForm
from .models import Category, Gig

# Payment Imports

import random
from os import environ
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from zeep import Client


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

# Payment Shits


class PaymentView(View):
    template_name = 'gigs/payment.html'
    messages = {
        "invalid_amount": {
            "level": messages.ERROR,
            "text": "Invalid Amount"
        },
        "get_token_fail": {
            "level": messages.ERROR,
            "text": "Get Token Failed : %s"
        },
    }

    def post(self, request, id):

        gig = get_object_or_404(Gig, id=id)
        amount = round(gig.price)
        order_id = random.random()

        if amount:
            client = Client('https://api.nextpay.org/gateway/token.wsdl')
            result = client.service.TokenGenerator(
                environ.get('PAYMENT_API_KEY'),
                order_id,
                amount,
                request.build_absolute_uri(reverse('gigs:payment_callback')),
            )

            if result.code != -1:
                messages.add_message(
                    self.request,
                    self.messages["get_token_fail"]["level"],
                    self.messages["get_token_fail"]["text"] % result.code
                )
            else:
                return redirect('https://api.nextpay.org/gateway/payment/%s' % result.trans_id)

        else:
            messages.add_message(
                self.request,
                self.messages["invalid_amount"]["level"],
                self.messages["invalid_amount"]["text"]
            )

        return redirect(self.get_fail_url())

    def get_fail_url(self):
        return str(reverse_lazy('gigs:payment'))

    def get_success_url(self):
        return str(reverse_lazy('gigs:payment'))


class PaymentCallbackView(View):
    template_name = 'gigs/callback.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCallbackView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        trans_id = request.POST.get('trans_id')
        order_id = request.POST.get('order_id')

        amount = 2000

        if trans_id and order_id and amount:
            client = Client('https://api.nextpay.org/gateway/verify.wsdl')
            result = client.service.PaymentVerification(
                environ.get('PAYMENT_API_KEY'),
                order_id,
                amount,
                trans_id,
            )

            return render(request, self.template_name, {
                'result_code': result,
                'trans_id': trans_id
            })

        else:
            return HttpResponseBadRequest()


# """
