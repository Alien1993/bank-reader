from django.core.management.base import BaseCommand
from django.conf import settings

from scrapy.crawler import CrawlerProcess

from scraper.spider import FinecoSpider


class Command(BaseCommand):
    help = "Launches spider to retrieve bank movements"

    def handle(self, *args, **options):
        process = CrawlerProcess(settings.SCRAPY_SETTINGS)
        process.crawl(FinecoSpider)
        process.start()
