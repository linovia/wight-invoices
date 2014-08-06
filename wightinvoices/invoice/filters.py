import django_filters
from . import models


class Estimate(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[('', 'All')] + [e[:2] for e in models.ESTIMATE_STATUS])
    class Meta:
        model = models.Estimate
        fields = ['client', 'name', 'status']
