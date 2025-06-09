from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from datetime import datetime
from pymongo import MongoClient
import scrapy
import os
import tempfile  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class nkuhistorySpider(CrawlSpider): 
    name = "nkuhistorySpider"         
    allowed_domains = ["history.nankai.edu.cn"]
    start_urls = ["http://history.nankai.edu.cn"]

    rules = (
        Rule(
            LinkExtractor(allow=(), deny_extensions=[]),
            callback="parse_item",
            follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(nkuhistorySpider, self).__init__(*args, **kwargs)
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['NKU']
        self.collection = self.db['nku']   
        self.page_id = 1

        chrome_options = Options()
        chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        user_data_dir = tempfile.mkdtemp(prefix="chrome_user_data_")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        self.snapshot_dir = "./snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def parse_item(self, response):
        if response.status != 200 or "Not Found" in response.text:
            return

        url = response.url
        if self.collection.find_one({'url': url}):
            return

        item = NkuspiderItem()
        item['url'] = url
        item['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['title'] = response.xpath('//title/text()').get(default='').strip()

        texts = response.xpath('//body//text()').getall()
        content = '\n'.join([t.strip() for t in texts if t.strip()])
        item['content'] = content

        item['source_type'] = 'history' 
        item['page_links'] = list(set(response.css("a::attr(href)").getall()))

        snapshot_name = f"history_{self.page_id}.png"
        item['snapshot_filename'] = snapshot_name
        self.save_snapshot(url, snapshot_name)

        self.page_id += 1
        yield item

    def save_snapshot(self, url, snapshot_name):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            filepath = os.path.join(self.snapshot_dir, snapshot_name)
            self.driver.save_screenshot(filepath)
            print(f"[快照] 已保存：{filepath}")
        except Exception as e:
            print(f"[错误] 快照保存失败：{url} - {e}")

    def closed(self, reason):
        try:
            self.client.close()
        except Exception as e:
            print(f"[关闭 MongoDB 连接出错] {e}")
        try:
            self.driver.quit()
        except Exception as e:
            print(f"[关闭浏览器驱动出错] {e}")
