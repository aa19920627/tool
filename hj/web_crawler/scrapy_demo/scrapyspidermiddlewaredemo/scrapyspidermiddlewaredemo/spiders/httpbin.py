import scrapy
from loguru import logger
from scrapy import Request

from ..items import DemoItem


class HttpbinSpider(scrapy.Spider):
    name = "httpbin"
    allowed_domains = ["www.httpbin.org"]
    start_urls = "https://www.httpbin.org/get"

    async def start(self):
        for i in range(5):
            url = f'{self.start_urls}?query={i}'
            logger.info(f'Requesting {url}')
            yield Request(url, callback=self.parse)

    def parse(self, response):
        item = DemoItem(**response.json())
        print('Status', response.status)
        yield item
