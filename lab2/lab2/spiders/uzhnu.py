import scrapy
from bs4 import BeautifulSoup
from lab2.items import FacultyItem


class UzhnuSpider(scrapy.Spider):
    # ім'я павука повинно співпадати з іменем файлу та входити до імені класу
    name = "uzhnu"
    allowed_domains = ["uzhnu.edu.ua"]
    # список адрес сторінок з яких починається скрапінг
    start_urls = ["https://uzhnu.edu.ua/uk/cat/faculty"]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        # знаходимо список факультетів і для кожного факультету
        fac_list = soup.find(class_="departments_unfolded")
        for li in fac_list.find_all("li"):
            a = li.find("a")
            # в <a> знаходимо ім'я і посилання на сторінку факультету
            fac_name = a.find(string=True, recursive=False)
            fac_link = f"https://uzhnu.edu.ua/{a.get('href')}"
            yield FacultyItem(
                name=fac_name,
                url=fac_link
            )
