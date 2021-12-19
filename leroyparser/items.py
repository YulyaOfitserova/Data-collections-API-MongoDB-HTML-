# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from itemloaders.processors import TakeFirst, MapCompose
import scrapy


def float_value(itm):
    try:
        return float(itm)   # обработка price
    except:
        return itm


def clear_value(itm):
    try:
        return re.sub(r'(\n[ \t]*)+', '', itm)     # обработка полей характеристик
    except:
        return itm


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(float_value))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    key = scrapy.Field()
    value = scrapy.Field(input_processor=MapCompose(clear_value))
    specifications = scrapy.Field()
    _id = scrapy.Field()
