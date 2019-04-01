from rest_framework import serializers

from scraper.models import Movement


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = (
            "id",
            "date",
            "description",
            "category",
            "sub_category",
            "amount",
            "amount_currency",
        )
        read_only_fields = (
            "id",
            "date",
            "description",
            "category",
            "sub_category",
            "amount",
            "amount_currency",
        )
