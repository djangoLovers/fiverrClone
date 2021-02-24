from django.db.models import fields
import django_filters

from .models import Gig


class gigFilter(django_filters.FilterSet):
    class Meta:
        model = Gig
        fields = ['category']
