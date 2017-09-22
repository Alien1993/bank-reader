import os

from moneyed import Money

from .exceptions import CurrencyException


def _get_env_var(key):
    try:
        return os.environ[key]
    except KeyError:
        raise KeyError("Missing env var {}".format(key))


def get_username():
    return _get_env_var("BANK_READER_USERNAME")


def get_password():
    return _get_env_var("BANK_READER_PASSWORD")


def convert_amount(amount):
    """ Utility function that converts an amount formatted like '1.000,00€' to Money object """
    currencies = {'€': 'EUR'}

    # Removes dots and converts commas to dots and removes currency symbol
    money = amount.replace('.', '').replace(',', '.')[:-1]

    symbol = amount[-1:]
    # Tries to get currency code
    try:
        currency = currencies[symbol]
    except KeyError:
        # TODO: Add logging
        raise CurrencyException('Unknown currency: %s' % symbol)

    return Money(amount=money, currency=currency)
