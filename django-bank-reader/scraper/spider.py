from datetime import datetime, date, timedelta
import os
import logging

import scrapy
import scrapy_splash

from .exceptions import CurrencyException
from .models import Movement
from .utils import get_username, get_password, convert_amount


logger = logging.getLogger(__name__)


class FinecoSpider(scrapy.Spider):
    """ Spider crawling Fineco site to parse list of movements """
    BASE_URL = 'https://finecobank.com/'
    LOGIN_URL = BASE_URL + 'it/public/'
    MONEYMAP_URL = BASE_URL + 'conto-e-carte/bilancio-familiare'
    LOSSES_URL = BASE_URL + 'conto-e-carte/bilancio-familiare/movimenti-tutti-uscite/'
    REVENUES_URL = BASE_URL + 'conto-e-carte/bilancio-familiare/movimenti-tutti-entrate/'

    name = "FinecoSpider"
    start_urls = [LOGIN_URL]

    def __init__(self, name=None, **kwargs):
        super(FinecoSpider, self).__init__(name, **kwargs)
        # Reads Splash lua scripts
        file_dir = os.path.dirname(os.path.realpath(__file__))
        with open(file_dir + '/login.lua', 'r') as login_lua:
            self.login_lua = login_lua.read()
        with open(file_dir + '/movements.lua', 'r') as movements_lua:
            self.movements_lua = movements_lua.read()

    def parse(self, response):
        return scrapy_splash.SplashFormRequest.from_response(
            response,
            formdata={'LOGIN': get_username(), 'PASSWD': get_password()},
            callback=self.after_login,
            endpoint='execute',
            args={'lua_source': self.login_lua}
        )

    def after_login(self, response):
        """ Makes first requests to get movements after sucessful login """
        if ('error' in response.url):
            msg = "Failed login"
            logger.warn(msg)
            raise scrapy.exceptions.CloseSpider(reason=msg)

        last_movement_date = Movement.get_last_date()
        # If no Movement has ever been parsed set start date to June 2015 else
        # sets it to some days before the last movement date
        if (last_movement_date == date.min):
            last_movement_date = date(2015, 6, 1)
        else:
            last_movement_date = last_movement_date - timedelta(days=3)

        # Starts parsing of losses
        losses_request = scrapy_splash.SplashRequest(
            url=self.LOSSES_URL,
            callback=self.parse_movements,
            endpoint='execute',
            cache_args=['lua_source'],
            dont_filter=True,
            args={
                'lua_source': self.movements_lua,
                'moneymap_url': self.MONEYMAP_URL,
                'meseanno': last_movement_date.strftime('%m%Y'),
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            meta={'date': last_movement_date}
        )

        # Starts parsing of revenues
        revenues_request = scrapy_splash.SplashRequest(
            url=self.REVENUES_URL,
            callback=self.parse_movements,
            endpoint='execute',
            cache_args=['lua_source'],
            dont_filter=True,
            args={
                'lua_source': self.movements_lua,
                'moneymap_url': self.MONEYMAP_URL,
                'meseanno': last_movement_date.strftime('%m%Y'),
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            meta={'date': last_movement_date}
        )
        revenues_request.meta['date'] = last_movement_date

        return [losses_request, revenues_request]

    def parse_movements(self, response):
        """ Parses a list of movements and saves them in DB if it doesn't already exists """

        # Gets description of all movements
        movements = response.xpath('//tr[contains(@class, "description")]')
        for movement in movements:
            row = movement.xpath('.//td')
            for i, cell in enumerate(row):
                if i == 1:
                    timestamp = cell.xpath('text()').extract_first().strip()
                    movement_date = datetime.strptime(timestamp, '%d/%m/%Y')
                elif i == 2:
                    description = cell.xpath('.//b/text()').extract_first().strip()
                elif i == 3:
                    category = cell.xpath('text()').extract_first().strip()
                    sub_category = cell.xpath('.//i/text()').extract_first().strip()
                elif i == 5:
                    # If currency is unknown skips current movement
                    try:
                        amount = convert_amount(cell.xpath('.//b/text()').extract_first().strip())
                    except CurrencyException as exc:
                        msg = 'Skipping movement {} of {}. {}'.format(description, movement_date, exc)
                        logger.exception(msg)
                        break

            # Losses are saved as negative values
            if response.url == self.LOSSES_URL:
                amount = -amount

            # Creates new Movement if it doesn't already exists
            Movement.objects.get_or_create(
                date=movement_date,
                description=description,
                category=category,
                sub_category=sub_category,
                amount=amount)

        # If last month parsed is current one returns since I might be dead by the night
        today = date.today()
        if (response.meta['date'].year == today.year and
                response.meta['date'].month == today.month):
            return

        # A call might fail from time to time since Splash container crashes
        # randomly and needs to restart, if that happens the page can't be
        # scraped so the call must be repeated for that same month
        if response.status == 200:
            next_month = response.meta['date'] + timedelta(weeks=4)
        else:
            next_month = response.meta['date']

        # Creates request to get next month movements
        request = scrapy_splash.SplashRequest(
            response.url,
            callback=self.parse_movements,
            endpoint='execute',
            cache_args=['lua_source'],
            dont_filter=True,
            args={
                'lua_source': self.movements_lua,
                'moneymap_url': self.MONEYMAP_URL,
                'meseanno': response.meta['date'].strftime('%m%Y'),
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            meta={'date': next_month}
        )
        return [request]
