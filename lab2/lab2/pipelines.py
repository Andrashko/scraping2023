# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from re import search
from scrapy.exceptions import DropItem
from lab2.items import StaffItem

class CleanNamePipeline:
    def process_item(self, item, spider):
        # очищуємо імена тільки викладачів. 
        # З іншими результатами (кафедрами і факультетами) не робимо нічого
        if not isinstance(item, StaffItem):
            return item
        name = item.get("name")
        # шукаємо підрядок за шаблоном "Андрашко Юрій Васильович"
        res = search(
            r"[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ][а-яіїє\']+",
            name
        )
        # якщо не вдалось, то шукаємо підрядок за шаблоном "Андрашко Ю. В."
        if not res:
            res = search(
                r"[А-ЯІЇЄ][а-яіїє\']+\s[А-ЯІЇЄ]\.\s?[А-ЯІЇЄ]\.",
                name
            )
        # якщо не вдалось знайти ім’я за жодним із шаблонів то працівника не розглядаємо 
        if not res:
            raise DropItem(f"Bad name {name}")
        # замінюємо ім'я знайденим підрядком і опрацьовуємо далі
        item["name"] = res.group(0)
        return item

