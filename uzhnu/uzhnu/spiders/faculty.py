import scrapy
from bs4 import BeautifulSoup
from uzhnu.items import UzhnuItem


class FacultySpider(scrapy.Spider):
    name = "faculty"
    allowed_domains = ["uzhnu.edu.ua"]
    start_urls = ["https://uzhnu.edu.ua/uk/cat/faculty"]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        fac_list = soup.find(class_="departments_unfolded")
        for li in fac_list.find_all("li"):
            a = li.find("a")
            fac_name = a.find(string=True, recursive=False)
            fac_link = "https://uzhnu.edu.ua" + a.get("href")
            yield UzhnuItem(
                name= fac_name,
                url = fac_link
            )

            yield scrapy.Request(url=fac_link, callback=self.DEP_parse)
    
    def DEP_parse(self, response):
        pass
