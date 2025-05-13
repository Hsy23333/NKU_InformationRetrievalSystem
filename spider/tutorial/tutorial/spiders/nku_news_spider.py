from scrapy import Request
from ..items import *
from datetime import datetime
from pymongo import MongoClient
import scrapy
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class nkunewsspider(scrapy.Spider):
    name = "nkunewsspider"
    allowed_domains = ["news.nankai.edu.cn"]
    start_urls = ["https://news.nankai.edu.cn/ywsd/system/index.shtml"]

    def __init__(self, *args, **kwargs):
        super(nkunewsspider, self).__init__(*args, **kwargs)
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['NKU']
        self.collection = self.db['nkunews']
        self.jump_num = 0

        # Selenium 设置
        CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        chrome_options = Options()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # 更改快照目录
        self.snapshot_dir = "./newssnapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def parse(self, response):
        if response.status != 200:
            return

        # 如果当前是目标新闻页面
        if response.url.endswith('.shtml'):
            if self.collection.find_one({'url': response.url}):
                self.jump_num += 1
                print(f"[跳过] 已存在：{response.url}")
                return

            item = NkuspiderItem()
            item['url'] = response.url
            item['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['title'] = response.xpath('//title/text()').get(default='').strip()

            texts = response.xpath('//body//text()').getall()
            content = '\n'.join([t.strip() for t in texts if t.strip()])
            item['content'] = content

            item['page_links'] = self.get_page_links(response)

            page_id = os.path.basename(response.url).replace('.shtml', '')
            self.save_snapshot(response.url, page_id)

            yield item

        # 继续发现其他新闻链接
        for href in response.xpath('//a/@href').getall():
            abs_url = response.urljoin(href)
            if self.is_valid_news_url(abs_url):
                yield Request(url=abs_url, callback=self.parse)

    def is_valid_news_url(self, url):
        return (
            url.startswith("https://news.nankai.edu.cn/ywsd/system/")
            and url.endswith(".shtml")
        )

    def get_page_links(self, response):
        links = response.xpath('//a/@href').getall()
        filtered = [
            response.urljoin(link) for link in links
            if link.startswith("/ywsd/system/") and link.endswith(".shtml")
        ]
        return list(set(filtered))

    def save_snapshot(self, url, page_id):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            filepath = os.path.join(self.snapshot_dir, f"{page_id}.png")
            self.driver.save_screenshot(filepath)
            print(f"[快照] 已保存：{filepath}")
        except Exception as e:
            print(f"[错误] 快照保存失败：{url} - {e}")

    def closed(self, reason):
        self.client.close()
        self.driver.quit()
