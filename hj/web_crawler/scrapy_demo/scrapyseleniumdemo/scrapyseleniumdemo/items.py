# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyseleniumdemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    name = scrapy.Field()
    tags = scrapy.Field()
    score = scrapy.Field()
    cover = scrapy.Field()
    price = scrapy.Field()


