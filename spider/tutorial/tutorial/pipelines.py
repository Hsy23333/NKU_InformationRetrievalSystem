import pymongo
from itemadapter import ItemAdapter

class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_database, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_database = mongo_database
        self.mongo_collection = mongo_collection
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 从 Scrapy settings 获取 MongoDB 配置
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_database=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        # 在爬虫启动时建立 MongoDB 连接
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_database]

    def close_spider(self, spider):
        # 在爬虫结束时关闭 MongoDB 连接
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        # 将抓取的 item 插入到 MongoDB
        collection = self.db[self.mongo_collection]
        collection.insert_one(dict(item))  # 插入数据到指定集合
        return item
