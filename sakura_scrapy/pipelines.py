# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import pymongo
import pymysql 
from twisted.enterprise import adbapi
from scrapy.http import Request



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
            

class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'sakura1')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        #port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'lsq123456')
        # self.db_conn = pymysql.connect(host, user, passwd, db)
        # self.db_cur = self.db_conn.cursor()
        self.dbpool = adbapi.ConnectionPool('pymysql', host=host, db=db,user=user, passwd=passwd)

    def close_spider(self, spider):
        # self.db_conn.commit()
        # self.db_conn.close()
        self.dbpool.close()

    def process_item(self, item, spider):
        # self.insert_db(item)
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    """ def insert_db(self, item):
        values = (
            item['video_id'],
            item['video_name'],
            item['video_aliasname'],
            item['video_updateinfo'],
            item['video_region'],
            item['video_type'],
            item['video_years'],
            item['video_tag'],
            item['video_index'],
            item['video_desc'],
            item['video_detailurl'],
            item['video_episodeurl']
        )
        sql = 'INSERT INTO video VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values) """

    def insert_db(self, tx, item):
        values = (
            item['video_id'],
            item['video_name'],
            item['video_aliasname'],
            item['video_updateinfo'],
            item['video_region'],
            item['video_type'],
            item['video_years'],
            item['video_tag'],
            item['video_index'],
            item['video_desc'],
            item['video_detailurl'],
            item['video_episodeurl'],
            item['video_picurl']
        )
        sql = 'INSERT INTO video VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)

class VideoPicPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x,meta={'videoitem':item}) for x in item.get(self.images_urls_field, [])]
    def file_path(self, request, response=None, info=None):
        videoitem = request.meta["videoitem"]
        img_id = videoitem['video_id']
        img_region = videoitem['video_region']
        return 'test/%s/%s.jpg' % (img_region,img_id)