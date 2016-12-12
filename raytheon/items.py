# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaytheonItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    reqid = scrapy.Field()
    location = scrapy.Field()
    applink = scrapy.Field()
    description = scrapy.Field()
    clearance = scrapy.Field()
    clearanceAndJunk = scrapy.Field()

