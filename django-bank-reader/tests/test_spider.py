from datetime import date

import pytest
import scrapy

from factories import MovementFactory
from scraper.spider import FinecoSpider


@pytest.mark.django_db()
def test_after_login_with_movements(mocker):
    """
    Verifies FormRequests are created with expected date after login with
    Movements saved in DB
    """
    # Saves some Movement in DB
    MovementFactory(date=date(2016, 6, 6))
    MovementFactory(date=date(2016, 6, 7))
    MovementFactory(date=date(2016, 6, 18))
    MovementFactory(date=date(2016, 7, 5))

    # Creates spider
    spider = FinecoSpider()

    # Gets requests created after login
    response = mocker.Mock()
    response.url = 'some url'
    losses_requests, revenues_request = spider.after_login(response)

    # Verifies losses requests is created as expected
    assert FinecoSpider.LOSSES_URL in str(losses_requests)
    assert 'meseanno=072016' in losses_requests.body.decode()
    assert 'dopoAggiornamento=false' in losses_requests.body.decode()
    assert 'idBrand=' in losses_requests.body.decode()
    assert losses_requests.meta['date'] == date(2016, 7, 2)

    # Verifies revenues requests is created as expected
    assert FinecoSpider.REVENUES_URL in str(revenues_request)
    assert 'meseanno=072016' in revenues_request.body.decode()
    assert 'dopoAggiornamento=false' in revenues_request.body.decode()
    assert 'idBrand=' in revenues_request.body.decode()
    assert revenues_request.meta['date'] == date(2016, 7, 2)


@pytest.mark.django_db()
def test_after_login_without_movements(mocker):
    """
    Verifies FormRequests are created with expected date after login with no
    Movement saved in DB
    """
    # Creates spider
    spider = FinecoSpider()

    # Gets requests created after login
    response = mocker.Mock()
    response.url = 'some url'
    losses_requests, revenues_request = spider.after_login(response)

    # Verifies losses requests is created as expected
    assert FinecoSpider.LOSSES_URL in str(losses_requests)
    assert 'meseanno=062015' in losses_requests.body.decode('utf-8')
    assert 'dopoAggiornamento=false' in losses_requests.body.decode('utf-8')
    assert 'idBrand=' in losses_requests.body.decode('utf-8')
    assert losses_requests.meta['date'] == date(2015, 6, 1)

    # Verifies revenues requests is created as expected
    assert FinecoSpider.REVENUES_URL in str(revenues_request)
    assert 'meseanno=062015' in revenues_request.body.decode('utf-8')
    assert 'dopoAggiornamento=false' in revenues_request.body.decode('utf-8')
    assert 'idBrand=' in revenues_request.body.decode('utf-8')
    assert revenues_request.meta['date'] == date(2015, 6, 1)


def test_after_failed_login(mocker):
    """ Verifies exception is raised on failed login """
    # Creates spider
    spider = FinecoSpider()

    # Gets requests created after login
    response = mocker.Mock()
    response.url = 'error'
    with pytest.raises(scrapy.exceptions.CloseSpider) as exc:
        spider.after_login(response)
    assert 'Failed login' in str(exc.value.reason)
