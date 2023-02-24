from requests import get
from bs4 import BeautifulSoup


BASE_URL = "https://hotline.ua"
URL = f"{BASE_URL}/ua/computer/noutbuki-netbuki/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
LAST_PAGE = 443

# відкриваємо файл
FILE_NAME = "laptops.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for p in range(1, LAST_PAGE):
        # надсилаємо параметр сторінки
        page = get(URL, headers=HEADERS, params={"p": p})
        soup = BeautifulSoup(page.content,  "html.parser")

        # знаходимо список товарів
        items = soup.find(
            name="div", class_="list-body__content").find_all(class_="list-item")
        # Для кожного товару
        for item in items:
            # Знаходимо назву
            title = item.find(
                name="a", class_="list-item__title").find(string=True, recursive=False).strip()
            # та ціну
            price = item.find(class_="price__value").find(
                string=True, recursive=False)

            print(f"Назва: {title}")
            print(f"Ціна: {price}")
            file.write(f"Назва: {title}\n")
            file.write(f"Ціна: {price}\n")
