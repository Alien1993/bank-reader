import datetime
from decimal import Decimal

import factory

from scraper import models


class MovementFactory(factory.django.DjangoModelFactory):
    """ Creates Movement used for testing """
    class Meta:
        model = models.Movement

    date = datetime.date.today()
    description = "Lunch"
    category = "Food"
    sub_category = "Food"
    amount = Decimal(15)
    currency = models.Movement.EUR
