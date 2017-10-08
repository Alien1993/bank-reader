from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess

from scraper.spider import FinecoSpider


class Command(BaseCommand):
    help = "Launches spider to retrieve bank movements"

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(FinecoSpider)
        process.start()
