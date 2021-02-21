from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Gig, Category
from .forms import GigForm


def index(request):
    gigs = Gig.objects.all()
    context = {'title': 'Gigs', 'gigs': gigs}
    return render(request, 'gigs/index.html', context)


def show(request, id):
    gig = Gig.objects.get(id=id)
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
            return redirect('gigs:show', newForm.id)
        else:
            messages.error(request, 'Somthing Went Wrong ..')

    context = {'title': 'New Gig', 'form': form, 'categorys': categorys}
    return render(request, 'gigs/new.html', context)


@login_required(login_url='/accounts/google/login/')
def edit(request, id):
    gig = Gig.objects.get(id=id)
    Categorys = Category.objects.all()
    gigCategorys = Category.objects.filter(gig=gig.id)
    context = {
        'title': f'Editing {gig.name}', 'gig': gig,
        'categorys': Categorys, 'gigCategorys': gigCategorys
    }
    print(gigCategorys)
    return render(request, 'gigs/edit.html', context)
