import scrapy


class UzhnuSpider(scrapy.Spider):
    name = "uzhnu"
    allowed_domains = ["uzhnu.edu.ua"]
    start_urls = ["http://uzhnu.edu.ua/"]

    def parse(self, response):
        pass
