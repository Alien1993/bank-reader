from django_filters import rest_framework as filters

from scraper.models import Movement


class MovementDateRangeFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="date", lookup_expr="lte")
    amount_from = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_to = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Movement
        fields = ["date_from", "date_to", "amount_from", "amount_to"]
