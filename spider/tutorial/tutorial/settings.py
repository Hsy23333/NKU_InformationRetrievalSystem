# Scrapy settings for tutorial project

BOT_NAME = "tutorial"

SPIDER_MODULES = ["tutorial.spiders"]
NEWSPIDER_MODULE = "tutorial.spiders"

ROBOTSTXT_OBEY = False

#UA 伪装
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


COOKIES_ENABLED = True

DOWNLOAD_DELAY = 0.1  #s

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


ITEM_PIPELINES = {
    'tutorial.pipelines.MongoDBPipeline': 1,
}

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'NKU'
MONGO_COLLECTION = 'nku'

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
