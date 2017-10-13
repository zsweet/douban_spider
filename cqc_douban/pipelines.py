# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cgi import log

import pymongo
from bson import ObjectId


class CqcDoubanPipeline(object):
    def __init__(self, mongo_uri, mongo_db,mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI1'),
            mongo_db=crawler.settings.get('MONGO_DB1'),
            mongo_col=crawler.settings.get('MONGO_COL1')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[ self.mongo_col ]

    def process_item(self, item, spider):
        condition = {'id' : item['id']}
       # condition = {'country':'美国'}
        newdata = {
            'actors':item['actors'],
            'director': item['director'],
            'screenwriter': item['screenwriter'],
            'country': item['country'],
            'dateCountry': item['dateCountry'],
            'language': item['language'],
            'duration': item['duration'],
            'nickname':item['nickname'],
            'imdb': item['imdb'],
            'kind': item['kind'],
            'comments': item['comments'],
            'reviews': item['reviews'],
            'rating': item['rating'],
            'rating_sum': item['rating_sum'],
            'rating_per': item['rating_per'],
            'rating_betterthan': item['rating_betterthan'],
            'id':item['id'] ,
            'source' : item['source'],
            'content' : item['content'],
            'title' : item['title'],
            'tags' : item['tags'],
            'url' : item['url'],
           # 'test':'aaabbb'
          }

       # self.db.getMongo().setSlaveOk();
        try:
            #print('!!!!!!!!!!!!!!!!!!!')
            #print(item['_id'])
            #print(condition)
            #self.db['quotes'].insert(newdata)
           # print(newdata)
            self.collection.insert(newdata)
           # self.collection.update_many( condition ,{'$set': newdata},False,False )
        except BaseException as e:
            print('Reason:')
            print(e)
        return item

    def close_spider(self, spider):
        self.client.close()

