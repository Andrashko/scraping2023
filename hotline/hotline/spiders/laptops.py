import scrapy
from bs4 import BeautifulSoup
from hotline.items import HotlineItem


class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["hotline.ua"]
    start_urls = [
        f"https://hotline.ua/ua/computer/noutbuki-netbuki/?p={page}" for page in range(1, 2)]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")

        # знаходимо список товарів
        items = soup.find(
            name="div", class_="list-body__content").find_all(class_="list-item")
        # Для кожного товару
        for item in items:
            # Знаходимо назву
            name = item.find(name="a", class_="list-item__title").find(
                string=True, recursive=False).strip()
            # url
            url = item.find(name="a", class_="list-item__title").get("href")
            # та ціну
            price = item.find(class_="price__value").find(
                string=True, recursive=False)
            # url картинки
            image_url = item.find(name="img").get("src")
            # повертаємо результат
            yield HotlineItem(
                name=name,
                price=price,
                url=url,
                image_urls=[f"https://hotline.ua{image_url}"]
            )
