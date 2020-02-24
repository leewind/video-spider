# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .items import SpiderXigua
import urllib
import pymongo

class SpiderPipeline(object):

    username_str = 'breadt'
    password_str = 'Breadt@2019'

    def connect(self):

        username = urllib.parse.quote_plus(self.username_str)
        password = urllib.parse.quote_plus(self.password_str)

        self.client = pymongo.MongoClient('mongodb://%s:%s@192.168.31.87:27017/' % (username, password))
        self.db = self.client["ixigua"]

    def open_spider(self, spider):
        print('SpidersPipeline.open_spider')
        self.connect()

    def parse_content(self, item):
        for item in item['data']:
            one = self.db['video_info'].find_one({'item_id': item['item_id']})
            if one is None:
                self.db['video_info'].insert_one(item)

    def process_item(self, item, spider):
        data = []
        if isinstance(item, SpiderXigua):
            data = self.parse_content(item)

        return data

    def close_spider(self, spider):
        self.client.close()
