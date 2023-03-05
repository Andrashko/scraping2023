import scrapy
from hotline.items import HotlineItem


class LaptopsXpathSpider(scrapy.Spider):
    name = "laptops_xpath"
    allowed_domains = ["hotline.ua"]
    start_urls = [
        f"https://hotline.ua/ua/computer/noutbuki-netbuki/?p={page}" for page in range(1, 5)]

    def parse(self, response):
        # знаходимо список товарів
        items = response.xpath('//div[contains(@class, "list-body__content")]'
            ).xpath('.//*[contains(@class,"list-item")]')

        # Для кожного товару
        for item in items:
            # Знаходимо назву
            name = item.xpath('.//a[contains(@class,"list-item__title")]/text()').get()
            # url
            url = item.xpath('.//a[contains(@class,"list-item__title")]/@href').get()
            # та ціну
            price = item.xpath('.//*[@class="price__value"]/text()').get()
            # url картинки
            image_url = item.xpath('.//img/@src').get()
            # повертаємо результат
            yield HotlineItem(
                name=name,
                price=price,
                url=url,
                image_urls=[f"https://hotline.ua{image_url}"]
            )
