import datetime

import pytest

from scraper.models import Movement
from factories import MovementFactory


@pytest.mark.django_db()
def test_movement_get_last_date():
    """ Verifies last date is returned when at least one movement exists """

    # Creates some movements
    MovementFactory(date=datetime.date(2017, 2, 10))
    MovementFactory(date=datetime.date(2017, 1, 5))
    MovementFactory(date=datetime.date(2017, 4, 26))
    MovementFactory(date=datetime.date(2017, 3, 15))

    # Verifies date of last Movement is returned
    assert datetime.date(2017, 4, 26) == Movement.get_last_date()


@pytest.mark.django_db()
def test_movement_get_last_date_is_smallest():
    """ Verifies smallest date possible is returned when no movement exists """
    assert datetime.date.min == Movement.get_last_date()
