# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SplashProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productname = scrapy.Field()
    productprice = scrapy.Field()
    reviewcount = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
