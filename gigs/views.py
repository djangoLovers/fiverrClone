from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GigForm
from .models import Category, Gig


def index(request):
    gigs = Gig.objects.all()
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def show(request, id):
    gig = get_object_or_404(Gig, id=id)
    if request.method == 'POST':
        form = GigForm(request.POST or None, instance=gig)
        if form.is_valid():
            gig = form.save(commit=False)
            gig.user = request.user
            gig.save()
            messages.success(request, 'Gig Successfully Updated')
        else:
            messages.error(request, 'Somthing Went Wrong...')
    context = {'title': gig.name, 'gig': gig}
    return render(request, 'gigs/show.html', context)


@login_required(login_url='/accounts/google/login/')
def new(request):
    categorys = Category.objects.all()
    form = GigForm()
    if request.method == 'POST':
        form = GigForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.user = request.user
            newForm.save()
            messages.success(request, 'Gig Successfully Created')
            return redirect(newForm.get_absolute_url())
        else:
            messages.error(request, 'Somthing Went Wrong ..')
    context = {'title': 'New Gig', 'form': form, 'categorys': categorys}
    return render(request, 'gigs/new.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    gig = get_object_or_404(Gig, id=id)
    categories = Category.objects.all()
    gigCategorys = Category.objects.filter(gig=gig.id)
    context = {
        'title': f'Editing {gig.name}', 'gig': gig,
        'categorys': categories, 'gigCategorys': gigCategorys
    }
    return render(request, 'gigs/edit.html', context)
