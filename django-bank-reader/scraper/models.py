import datetime

from django.db import models


class Movement(models.Model):
    """ Model representing a bank movement """
    EUR = 'eur'
    USD = 'usd'
    CURRENCY_CHOICES = (
        (EUR, 'Euro'),
        (USD, 'US Dollar'),
    )
    date = models.DateField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES
    )

    def get_last_date():
        """ Convenience method to get date of last movement """
        last_movement = Movement.objects.order_by('date').last()
        if last_movement:
            return last_movement.date
        # If there's not Movement return the smallest date possible
        return datetime.date.min
