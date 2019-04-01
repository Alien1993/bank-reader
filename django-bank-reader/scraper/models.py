import datetime

from djmoney.models.fields import MoneyField
from django.db import models


class Movement(models.Model):
    """ Model representing a bank movement """

    date = models.DateField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency="EUR")

    def get_last_date():
        """ Convenience method to get date of last movement """
        last_movement = Movement.objects.order_by("date").last()
        if last_movement:
            return last_movement.date
        # If there's not Movement return the smallest date possible
        return datetime.date.min

    def __str__(self):
        return "Movement {}, amount: {}".format(self.date, self.amount)
