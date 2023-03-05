import scrapy
from bs4 import BeautifulSoup
from lab2.items import FacultyItem, DepartmentItem, StaffItem


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
            fac_url = f"https://uzhnu.edu.ua{a.get('href')}"
            # повертаємо дані про факультет
            yield FacultyItem(
                name=fac_name,
                url=fac_url
            )
            # також повертаємо запит для запуска скрапінгу кафедр на сторінці факультетету
            yield scrapy.Request(
                # адреса сторінки, яку необхідно парсити
                url=fac_url,
                # метод для обробки результатів завантаження
                callback=self.parse_faculty,
                # передаємо дані про факультет в функцію колбеку
                meta={
                    "faculty": fac_name
                }
            )

    def parse_faculty(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        dep_list = soup.find(class_="departments")
        # для кожної кафедри у списку
        if dep_list:
            for li in dep_list.find_all("li"):
                # знаходимо текст безпосередньо в контенті елементу  a
                dep_name = li.a.find(string=True, recursive=False)
                # URL кафедри
                dep_url = f"https://uzhnu.edu.ua{li.a.get('href')}"
                # повертаємо дані про кафедру
                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                    # факультет дізнаємось із метаданих, переданих при запиті
                    faculty=response.meta.get("faculty")
                )
                # також повертаємо запит для запуска скрапінгу працівників на сторінці кафедри
                yield scrapy.Request(
                    # адреса сторінки, яку необхідно парсити
                    url=dep_url,
                    # метод для обробки результатів завантаження
                    callback=self.parse_department,
                    # передаємо дані про кафедру в функцію колбеку
                    meta={
                        "department": dep_name
                    }
                )

    def parse_department(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        staff_list = soup.find(class_="page_block").ol
        # для кожного викладача у списку
        if staff_list:
            for li in staff_list.find_all("li"):
                # на деяких кафедрах ім'я - текст в пункті меню
                name = li.find(string=True, recursive=False)
                # на інших він додатково обгорнутий в <span>
                if not name and li.span:
                    name = li.span.find(string=True, recursive=False)
                # повертаємо дані про працівника
                yield StaffItem(
                    name=name,
                    department=response.meta.get("department")
                )
