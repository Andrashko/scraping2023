import scrapy
from bs4 import BeautifulSoup


class UzhnuSpider(scrapy.Spider):
    name = "uzhnu"
    allowed_domains = ["uzhnu.edu.ua"]
    start_urls = ["https://uzhnu.edu.ua/uk/cat/faculty"]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        fac_list = soup.find(class_="departments_unfolded")
        for li in fac_list.find_all("li"):
            a = li.find("a")
            fac_name = a.find(string=True, recursive=False)
            fac_link = "https://uzhnu.edu.ua/" + a.get("href")
            yield {
                "name": fac_name,
                "URL": fac_link
            }

