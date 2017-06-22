# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class House(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    dealDate = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    unitPrice = scrapy.Field()
    district = scrapy.Field()
    district_detail = scrapy.Field()
    base_property = scrapy.Field()
    deal_property = scrapy.Field()
    msg = scrapy.Field()
    pass
