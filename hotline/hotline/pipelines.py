# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem


class PricePipeline:
    def process_item(self, item, spider):
        try:
            item["price"] = float(item.get("price").replace("\xa0", ""))
            return item
        except:
            raise DropItem(f"Bad price in {item}")


class FilterPipeline:
    def filter(self, item):
        return "Apple" in item.get("name")

    def process_item(self, item, spider):
        if self.filter(item):
            raise DropItem(f"Item {item} by filter")
        return item


class DuplicatePipeline:
    def open_spider(self, spider):
        self.names = []

    def is_unique(self, name):
        return not (name in self.names)

    def process_item(self, item, spider):
        item_name = item.get("name")
        if self.is_unique(item_name):
            self.names.append(item_name)
            return item
        raise DropItem(f"Item {item} is duplicate")
