from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from scraper.models import Movement
from .serializers import MovementSerializer
from .filters import MovementDateRangeFilter


class MovementViewSet(ModelViewSet):
    queryset = Movement.objects.all().order_by("date")
    serializer_class = MovementSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = MovementDateRangeFilter
    search_fields = ("description", "category", "sub_category")
