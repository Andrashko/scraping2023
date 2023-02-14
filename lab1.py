from requests import get
from bs4 import BeautifulSoup


BASE_URL = "https://www.uzhnu.edu.ua"
URL = f"{BASE_URL}/uk/cat/faculty"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
page = get(URL, headers=HEADERS)
soup = BeautifulSoup(page.content,  "html.parser")
# елемент що має клас departments_unfolded
fac_list = soup.find(class_="departments_unfolded")
#для кожного дочірнього елемента li
for li in fac_list.find_all("li"):
    #дочірній елемент a
    a = li.find("a")
    #знаходимо текст безпосередньо в контенті елементу  a
    fac_name = a.find(text=True, recursive=False)
    #URL складається з базового, та відносного, який записано в атрибуті href
    fac_link = BASE_URL+ a.get("href")

    print(f"Назва факультету: {fac_name}")
    print(f"URL: {fac_link}")
