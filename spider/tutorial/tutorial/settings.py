# Scrapy settings for tutorial project

BOT_NAME = "tutorial"

SPIDER_MODULES = ["tutorial.spiders"]
NEWSPIDER_MODULE = "tutorial.spiders"

# 禁用 robots.txt，避免被拦截
ROBOTSTXT_OBEY = False

# 设置浏览器 UA 伪装
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

# 启用 cookies
COOKIES_ENABLED = True

# 设置请求延迟，降低访问频率
DOWNLOAD_DELAY = 0.1  # 单位为秒

# 启用 AutoThrottle 自适应限速
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# MongoDB pipeline
ITEM_PIPELINES = {
    'tutorial.pipelines.MongoDBPipeline': 1,
}

# MongoDB 设置
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'NKU'
MONGO_COLLECTION = 'nku'

# 编码与 Twisted 配置
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
