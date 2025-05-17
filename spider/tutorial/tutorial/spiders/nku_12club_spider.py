from scrapy import Request
from ..items import *
from datetime import datetime
from pymongo import MongoClient
import scrapy
import os

# 导入 Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # 可自动下载驱动

class nku12clubspider(scrapy.Spider):
    name = "nku12clubspider"

    def __init__(self, *args, **kwargs):
        super(nku12clubspider, self).__init__(*args, **kwargs)
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['NKU']
        self.collection = self.db['nku']
        self.jump_num = 0

        # 设置 Selenium 无头浏览器
        CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        chrome_options = Options()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # 快照保存路径
        self.snapshot_dir = "./snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def start_requests(self):
        base_url = "http://12club.nankai.edu.cn/programs/{}"
        for idx in range(1, 2710):  # 根据需要设置遍历编号范围
            url = base_url.format(idx)
            yield Request(url=url, callback=self.parse, meta={'page_id': idx})

    def parse(self, response):
        if response.status != 200 or "Not Found" in response.text:
            return  # 无效页面直接跳过

        page_id = response.meta['page_id']
        item = NkuspiderItem()
        item['url'] = response.url
        item['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['title'] = response.xpath('//title/text()').get(default='').strip()

        texts = response.xpath('//body//text()').getall()
        content = '\n'.join([t.strip() for t in texts if t.strip()])
        item['content'] = content

        if self.collection.find_one({'url': item['url']}):
            self.jump_num += 1
            print(f"[跳过] 已存在：{item['url']}")
            return

        item['page_links'] = self.get_page_links(response)

        
        item['snapshot_filename'] = f"12club_{page_id}.png"
        item['source_type'] = "12club"

        # 保存网页快照
        self.save_snapshot(response.url, page_id)

        yield item

    def get_page_links(self, response):
        links = response.xpath('//a/@href').getall()
        filtered = [
            response.urljoin(link) for link in links
            if link.startswith('/programs/')
        ]
        return list(set(filtered))

    def save_snapshot(self, url, page_id):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            filepath = os.path.join(self.snapshot_dir, f"12club_{page_id}.png")
            self.driver.save_screenshot(filepath)
            print(f"[快照] 已保存：{filepath}")
        except Exception as e:
            print(f"[错误] 快照保存失败：{url} - {e}")

    def closed(self, reason):
        self.client.close()
        self.driver.quit()
