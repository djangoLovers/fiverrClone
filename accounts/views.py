from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

#temporarly
def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})


class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    # These Next Two Lines Tell the View to Index
    # Lookups by Username
    slug_field = "full_name"
    slug_url_kwarg = "full_name"

user_detail_view = UserDetail.as_view()


class UserUpdate(LoginRequiredMixin, UpdateView):
    fields = [
        "short_bio",
        "description",
        "country",
    ]

    model = User


    def get_success_url(self):
        return reverse("users:detail", 
        kwargs={"full_name": self.request.user.full_name})


    # def get_object(self):
    #     # Only Get the User Record for the
    #     #   User Making the Request
    #     return User.objects.get(
    #         pk=self.request.user.pk
    #     )


user_update_view = UserUpdate.as_view()
