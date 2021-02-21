from django.shortcuts import redirect, render
from django.contrib import messages
from core.decorators import isLogged
from .models import Gig, Category
from .forms import GigForm


def index(request):
    if request.method == 'POST':
        form = GigForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            id = form.cleaned_data.get('id')
            newForm.user = request.user
            newForm.save()
            messages.success(request, 'Gig Successfully Created')
            return redirect('gigs:show', newForm.id)
        else:
            messages.error(request, 'Somthing Went Wrong ..')
            return redirect(new)

    gigs = Gig.objects.all()
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def show(request, id):
    gig = Gig.objects.get(id=id)
    context = {'title': gig.name, 'gig': gig}
    return render(request, 'gigs/show.html', context)


@isLogged
def new(request):
    categorys = Category.objects.all()
    form = GigForm()
    context = {'title': 'New Gig', 'form': form, 'categorys': categorys}
    return render(request, 'gigs/new.html', context)


def edit(request, id):
    gig = Gig.objects.get(id=id)
    context = {'title': f'Editing {gig.name}', 'gig': gig}
    return render(request, 'gigs/edit.html', context)
