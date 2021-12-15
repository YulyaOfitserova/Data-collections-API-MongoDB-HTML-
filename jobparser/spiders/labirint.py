import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BA%D0%BD%D0%B8%D0%B3%D0%B8/?stype=0',
                  'https://www.labirint.ru/search/%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BA%D0%BD%D0%B8%D0%B3%D0%B8/?stype=0']

    def parse(self, response):
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        author = response.xpath('//div[@class="authors"][text()="Автор: "]/a/text()').get()
        redactor = response.xpath('//div[@class="authors"][text()="Редактор: "]/a/text()').get()
        link = response.url
        price_now = response.xpath('//span[@class="buying-price-val" or @class="buying-pricenew-val-number"]//text()').get()
        price_old = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        currency = response.xpath('//span[@class="buying-pricenew-val-currency"]/text()').get()
        item = JobparserItem(name=name, author=author, redactor=redactor,
                             link=link, price_now=price_now, price_old=price_old, currency=currency)
        yield item


