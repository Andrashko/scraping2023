from requests import get


URL = "https://www.uzhnu.edu.ua/uk/cat/faculty"
page = get(URL)

print (page.text)
