# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item

class LocationItem(Item):
    lat = Field()
    lng = Field()
    addr = Field()

class GeopixnetItem(Item):
    # define the fields for your item here like:
    site_name = Field()
    url = Field()
    title = Field()
    desc = Field()
    location = LocationItem()


