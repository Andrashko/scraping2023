import scrapy
from hotline.items import HotlineItem


class LaptopsCssSpider(scrapy.Spider):
    name = "laptops_css"
    allowed_domains = ["hotline.ua"]
    start_urls = [
        f"https://hotline.ua/ua/computer/noutbuki-netbuki/?p={page}" for page in range(1, 5)]

    def parse(self, response):
        # знаходимо список товарів
        items = response.css('div.list-body__content').css('.list-item')

        # Для кожного товару
        for item in items:
            # Знаходимо назву
            name = item.css('a.list-item__title::text').get()
            # url
            url = item.css('a.list-item__title::attr(href)').get()
            # та ціну
            price = item.css('.price__value::text').get()
            # url картинки
            image_url = item.css('img::attr(src)').get()
            # повертаємо результат
            yield HotlineItem(
                name=name,
                price=price,
                url=url,
                image_urls=[f"https://hotline.ua{image_url}"]
            )
