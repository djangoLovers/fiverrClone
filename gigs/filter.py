import django_filters

from core.models import Gig


class gigFilter(django_filters.FilterSet):
    class Meta:
        model = Gig
        fields = ['category']
