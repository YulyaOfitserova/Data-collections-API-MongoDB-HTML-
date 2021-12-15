# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        if spider.name == 'book24':
            if not item['price_now'] is None:
                item['price_now'] = item['price_now'].replace('\xa0', '')
            if not item['price_old'] is None:
                item['price_old'] = item['price_old'].replace('\xa0', '')

        collection.insert_one(item)
        return item
