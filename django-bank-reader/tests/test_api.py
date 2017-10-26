import datetime

import pytest
from moneyed import Money
from rest_framework.reverse import reverse

from factories import MovementFactory


@pytest.mark.django_db
def test_movements_no_params(api_client):
    """
    Verifies all movements are returned when calling endpoint without paramaters
    """

    MovementFactory(date=datetime.date(2000, 2, 11))
    MovementFactory(date=datetime.date(2010, 2, 18))
    MovementFactory(date=datetime.date(2017, 1, 15))
    MovementFactory(date=datetime.date(2017, 5, 24))

    response = api_client.get(reverse('api:movements-list'))

    assert response.status_code == 200
    assert len(response.data) == 4
    assert response.data[0]['date'] == '2000-02-11'
    assert response.data[1]['date'] == '2010-02-18'
    assert response.data[2]['date'] == '2017-01-15'
    assert response.data[3]['date'] == '2017-05-24'


@pytest.mark.django_db
def test_movements_date_from(api_client):
    """
    Verifies correct movements are returned when calling endpoint with date_from
    parameter
    """

    MovementFactory(date=datetime.date(2017, 2, 10))
    MovementFactory(date=datetime.date(2017, 2, 11))

    response = api_client.get(reverse('api:movements-list'), {'date_from': '2017-02-11'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['date'] == '2017-02-11'


@pytest.mark.django_db
def test_movements_date_to(api_client):
    """
    Verifies correct movements are returned when calling endpoint with date_to
    parameter
    """

    MovementFactory(date=datetime.date(2017, 2, 10))
    MovementFactory(date=datetime.date(2017, 2, 11))

    response = api_client.get(reverse('api:movements-list'), {'date_to': '2017-02-10'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['date'] == '2017-02-10'


@pytest.mark.django_db
def test_movements_date_from_date_to(api_client):
    """
    Verifies correct movements are returned when calling endpoint with date_from
    and date_to parameter
    """

    MovementFactory(date=datetime.date(2017, 2, 9))
    MovementFactory(date=datetime.date(2017, 2, 10))
    MovementFactory(date=datetime.date(2017, 2, 11))
    MovementFactory(date=datetime.date(2017, 2, 12))

    response = api_client.get(
        reverse('api:movements-list'),
        {'date_from': '2017-02-10', 'date_to': '2017-02-11'}
    )

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['date'] == '2017-02-10'
    assert response.data[1]['date'] == '2017-02-11'


@pytest.mark.django_db
def test_movements_amount_from(api_client):
    """
    Verifies correct movements are returned when calling endpoint with amount_from
    parameter
    """

    MovementFactory(amount=Money(-10.00, 'EUR'))
    MovementFactory(amount=Money(50.00, 'EUR'))

    response = api_client.get(reverse('api:movements-list'), {'amount_from': -7})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['amount'] == '50.00'


@pytest.mark.django_db
def test_movements_amount_to(api_client):
    """
    Verifies correct movements are returned when calling endpoint with amount_to
    parameter
    """

    MovementFactory(amount=Money(-10.00, 'EUR'))
    MovementFactory(amount=Money(50.00, 'EUR'))

    response = api_client.get(reverse('api:movements-list'), {'amount_to': -7})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['amount'] == '-10.00'


@pytest.mark.django_db
def test_movements_amount_from_amount_to(api_client):
    """
    Verifies correct movements are returned when calling endpoint with amount_from
    and amount_to parameter
    """

    MovementFactory(amount=Money(-300.00, 'EUR'))
    MovementFactory(amount=Money(-10.00, 'EUR'))
    MovementFactory(amount=Money(50.00, 'EUR'))
    MovementFactory(amount=Money(1200.00, 'EUR'))

    response = api_client.get(
        reverse('api:movements-list'),
        {'amount_from': -20, 'amount_to': 50}
    )

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['amount'] == '-10.00'
    assert response.data[1]['amount'] == '50.00'


@pytest.mark.django_db
def test_movements_search(api_client):
    """
    Verifies correct movements are return when calling endpoint with search parameter
    """

    MovementFactory(description='Best Food Ever!', category='Lunch', sub_category='Lunch')
    MovementFactory(description='Booze Monday', category='Food', sub_category='Beer')
    MovementFactory(description='Kindle book', category='E-Commerce', sub_category='Book')
    MovementFactory(description='That cool restaurant', category='Restaurant', sub_category='Food')
    MovementFactory(description='Changed tires', category='Transport', sub_category='Car Repair')

    response = api_client.get(reverse('api:movements-list'), {'search': 'Food'})

    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['description'] == 'Best Food Ever!'
    assert response.data[0]['category'] == 'Lunch'
    assert response.data[0]['sub_category'] == 'Lunch'
    assert response.data[1]['description'] == 'Booze Monday'
    assert response.data[1]['category'] == 'Food'
    assert response.data[1]['sub_category'] == 'Beer'
    assert response.data[2]['description'] == 'That cool restaurant'
    assert response.data[2]['category'] == 'Restaurant'
    assert response.data[2]['sub_category'] == 'Food'
