# -*- coding: utf-8 -*-

import codecs
import json
import pymongo


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SakuraScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class WriteJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MongoDBPipeline(object):
    def open_spider(self, spider):

        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["sakura"]
        self.mycol = self.mydb["video"]

    def close_spider(self, spider):
        self.myclient.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item


    def insert_db(self, item):
        item = dict(item)
        self.mycol.insert_one(item)
            
