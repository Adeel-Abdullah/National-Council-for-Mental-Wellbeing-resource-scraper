# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from urllib.parse import urlparse

class ResourceScraperPipeline(FilesPipeline):
    def open_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)
        spider.logger.debug("PdfPipeline: open_spider")

    def close_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)
        spider.logger.debug("PdfPipeline: close_spider")
        
    def get_media_requests(self, item, info):
        pdf_url = item.get('pdf_url')
        info.spider.logger.debug(f"Downloading PDF: {pdf_url} as {item.get('pdf_filename')}")
        if pdf_url:
            yield scrapy.Request(pdf_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        pdf_name = item.get('pdf_filename')
        return os.path.join('pdfs', pdf_name)

    def item_completed(self, results, item, info):
        if not any(x['status'] == 'completed' for ok, x in results if ok):
            self.log_failed_download(item, info)
            raise DropItem(f"Failed to download PDF: {item['pdf_url']}")
        return item
    
    def log_failed_download(self, item, info):
        """Logs failed download to a file."""
        failed_downloads_file = 'failed_downloads.txt'
        with open(failed_downloads_file, 'w') as f:
            f.write(f"{item['pdf_url']}\n")

import json

from itemadapter import ItemAdapter


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("output\items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item) + "\n"
        self.file.write(line)
        return item
