from django.forms import ModelForm
from .models import Gig


class GigForm(ModelForm):
    class Meta:
        model = Gig
        exclude = ['user']
