import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5&section_id=2242',
                  'https://book24.ru/search/?q=%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5&section_id=2242']
    num_page = 2

    def parse(self, response, **kwargs):
        url = f'https://book24.ru/search/page-{self.num_page}/?q=%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5&section_id=2242'
        if url:
            yield scrapy.Request(url=url, callback=self.parse)
        links = response.xpath("//a[@class='product-card__image-link smartLink']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        self.num_page += 1

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        author = response.xpath('(//a[@class="product-characteristic-link smartLink"])[1]/text()').get()
        link = response.url
        price_now = response.xpath('//span[@class="app-price product-sidebar-price__price"]/text()').get()
        price_old = response.xpath('//span[@class="app-price product-sidebar-price__price-old"]/text()').get()
        rating = response.xpath('//span[@class="rating-widget__main-text"]/text()').get()
        item = JobparserItem(name=name, author=author,
                             link=link, price_now=price_now, price_old=price_old, rating=rating)
        yield item


