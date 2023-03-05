import scrapy
from bs4 import BeautifulSoup


class UzhnuSpider(scrapy.Spider):
    # ім'я павука повинно співпадати з іменем файлу та входити до імені класу
    name = "uzhnu"
    allowed_domains = ["uzhnu.edu.ua"]
    # список адрес сторінок з яких починається скрапінг
    start_urls = ["https://uzhnu.edu.ua/uk/cat/faculty"]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        #знаходимо список факультетів і для кожного факультету
        fac_list = soup.find(class_="departments_unfolded")
        for li in fac_list.find_all("li"):
            a = li.find("a")
            # з посилання знаходимо ім'я факультету і кафедри
            fac_name = a.find(string=True, recursive=False)
            fac_link = "https://uzhnu.edu.ua/" + a.get("href")
            yield {
                "name": fac_name,
                "URL": fac_link
            }
            