# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from mysql.connector import connect


class MySqlPipeline:
    def open_spider(self, spider):
        self.connection = connect(
            host="localhost",
            user="root",
            password=""
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL ")
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS scrapy;")
        self.cursor.execute("USE scrapy;")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(50) NOT NULL,
            price FLOAT DEFAULT 0,
            url VARCHAR(500)
        );""")
        spider.logger.info("DB is ready ")

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")

    def process_item(self, item, spider):
        if self.is_duplicate(item):
            raise DropItem(f"Item {item.get('name')} is already in database")
        self.cursor.execute(
            "INSERT INTO items (name, price, url) VALUES (%s, %s, %s);",
            [item.get("name"), item.get("price"), item.get("url")])
        self.connection.commit()
        return item

    def is_duplicate(self, item):
        self.cursor.execute(
            "SELECT COUNT(id) FROM items WHERE name = %s;",
            [item.get("name")])
        count = self.cursor.fetchone()[0]
        return count > 0


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
        self.duplicates = 0

    def is_unique(self, name):
        return not (name in self.names)

    def process_item(self, item, spider):
        item_name = item.get("name")
        if self.is_unique(item_name):
            self.names.append(item_name)
            return item

        self.duplicates += 1
        raise DropItem(f"Item {item_name} is duplicate")

    def close_spider(self, spider):
        spider.logger.debug(f"{self.duplicates} items were duplicated")
