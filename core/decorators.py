from django.shortcuts import redirect
from django.contrib import messages


def isLogged(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be Logged in !')
            return redirect('core:index')
    return wrapper


def notLogged(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        else:
            return view(request, *args, **kwargs)

    return wrapper
