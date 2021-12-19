import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={mark}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']//@data-origin")
        loader.add_xpath('key', "//dt[@class='def-list__term']/text()")   # левый стобец вкладки 'характеристики'
        loader.add_xpath('value', "//dd[@class='def-list__definition']//text()")  # правый стобец вкладки 'характеристики'
        yield loader.load_item()

