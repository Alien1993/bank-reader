import django_filters

from scraper.models import Movement


class MovementDateRangeFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(name='date', lookup_expr='lte')
    amount_from = django_filters.NumberFilter(name='amount', lookup_expr='gte')
    amount_to = django_filters.NumberFilter(name='amount', lookup_expr='lte')

    class Meta:
        model = Movement
        fields = ['date_from', 'date_to', 'amount_from', 'amount_to']
