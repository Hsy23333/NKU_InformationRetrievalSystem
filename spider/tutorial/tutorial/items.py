# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NkuspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    page_links = scrapy.Field()
    crawl_time = scrapy.Field()
    snapshot_filename=scrapy.Field()
    source_type = scrapy.Field()