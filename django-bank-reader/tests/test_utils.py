from decimal import Decimal

import pytest
from moneyed import EUR

from scraper.utils import convert_amount
from scraper.exceptions import CurrencyException


def test_convert_amount():
    """ Verifies amount is converted correctly """
    money = convert_amount('1.000,00€')
    assert money.amount == Decimal('1000.00')
    assert money.currency == EUR


def test_convert_amount_unknown_currency():
    """ Verifies exception is thrown if unknown currency is found """
    with pytest.raises(CurrencyException) as exc:
        convert_amount('1.000,00$')
    assert 'Unknown currency: $' in str(exc)
