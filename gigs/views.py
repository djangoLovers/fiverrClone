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
    context = {'title': gig.name, 'gig': gig}
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
        gigCategories = gig.category.all()
        form = GigForm(instance=gig)
        context = {
            'title': f'Editing {gig.name}', 'gig': gig,
            'categories': categories, 'gigCategories': gigCategories, 'form': form
        }
        return render(request, 'gigs/edit.html', context)
    else:
        messages.error(request, "You Don't have The Permission to do that")
        return redirect('core:index')
