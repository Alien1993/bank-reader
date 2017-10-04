from datetime import datetime, date, timedelta
import logging

import scrapy

from .exceptions import CurrencyException
from .models import Movement
from .utils import get_username, get_password, convert_amount


logger = logging.getLogger(__name__)


class FinecoSpider(scrapy.Spider):
    """ Spider crawling Fineco site to parse list of movements """
    BASE_URL = 'https://finecobank.com/'
    LOGIN_URL = BASE_URL + 'it/public/'
    LOSSES_URL = BASE_URL + 'conto-e-carte/bilancio-familiare/movimenti-tutti-uscite/'
    REVENUES_URL = BASE_URL + 'conto-e-carte/bilancio-familiare/movimenti-tutti-entrate/'

    name = "FinecoSpider"
    start_urls = [LOGIN_URL]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/59.0.3071.115 Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 2,
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'LOGIN': get_username(), 'PASSWD': get_password()},
            callback=self.after_login
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
        losses_request = scrapy.FormRequest(
            url=self.LOSSES_URL,
            formdata={
                'meseanno': last_movement_date.strftime('%m%Y'),
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            callback=self.parse_movements
        )
        losses_request.meta['date'] = last_movement_date

        # Starts parsing of revenues
        revenues_request = scrapy.FormRequest(
            url=self.REVENUES_URL,
            formdata={
                'meseanno': last_movement_date.strftime('%m%Y'),
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            callback=self.parse_movements
        )
        revenues_request.meta['date'] = last_movement_date

        return [losses_request, revenues_request]

    def parse_movements(self, response):
        """ Parses a movement and saves it in DB if it doesn't already exists """

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
                    sub_category = cell.xpath('.//i/text()').extract_first.strip()
                elif i == 5:
                    # If currency is unknown skips current movement
                    try:
                        amount = convert_amount(cell.xpath('.//b/text()').extract_first().strip())
                    except CurrencyException as exc:
                        msg = 'Skipping movement {} of {}. {}'.format(description, movement_date, exc)
                        logger.exception(msg)
                        break

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

        next_month = response.meta['date'] + timedelta(weeks=4)

        # Creates request to get next month movements
        request = scrapy.FormRequest.from_response(
            response,
            formdata={
                'meseanno': next_month,
                'dopoAggiornamento': 'false',
                'idBrand': ''
            },
            callback=self.parse_movements
        )
        request.meta['date'] = next_month
        return request
