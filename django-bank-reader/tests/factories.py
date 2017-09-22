import datetime

from moneyed import Money
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
    amount = Money(15, 'EUR')
