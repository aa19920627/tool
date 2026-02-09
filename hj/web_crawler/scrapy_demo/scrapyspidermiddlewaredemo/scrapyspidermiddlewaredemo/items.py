# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspidermiddlewaredemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DemoItem(scrapy.Item):
    origin = scrapy.Field()
    headers = scrapy.Field()
    args = scrapy.Field()
    url = scrapy.Field()

