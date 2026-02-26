# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch
from loguru import logger
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ScrapyitempipelinedemoPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.host = crawler.settings.get("MONGODB_HOST")
        cls.port = crawler.settings.get("MONGODB_PORT")
        cls.username = crawler.settings.get("MONGODB_USER")
        cls.password = crawler.settings.get("MONGODB_PASSWORD")
        cls.database = crawler.settings.get("MONGODB_DATABASE")
        cls.collection = crawler.settings.get('MONGODB_COLLECTION')

        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        self.db[self.collection].update_one(
            {
                'name': item['name']
            },
            {
                '$set': dict(item)
            },
            True
        )
        return item

    def close_spider(self, spider):
        self.client.close()


class ElasticsearchPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.connection_string = crawler.settings.get("ELASTICSEARCH_CONNECTION_STRING")
        cls.index = crawler.settings.get("ELASTICSEARCH_INDEX")
        return cls()

    def open_spider(self, spider):
        # 接字符串补充http协议
        conn_str = self.connection_string if self.connection_string.startswith(
            'http') else f"http://{self.connection_string}"
        self.conn = Elasticsearch([conn_str])

        # 直接创建索引（带基础配置+忽略已存在）
        index_config = {"settings": {"number_of_shards": 1}, "mappings": {"properties": {"name": {"type": "keyword"}}}}
        self.conn.indices.create(index=self.index, body=index_config, ignore=400)

    def process_item(self, item, spider):
        self.conn.index(index=self.index, body=dict(item), id=hash(item['name']))
        return item

    def close_spider(self, spider):
        self.conn.transport.close()


class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, item=None):
        movie = request.meta['movie']
        type = request.meta['type']
        name = request.meta['name']
        file_name = f'{movie}/{type}/{name}.jpg'
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item Downloaded Failed")
        return item

    def get_media_requests(self, item, info):
        for director in item['directors']:
            director_name = director['name']
            director_image = director['image']
            yield Request(director_image, meta={
                'name': director_name,
                'type': 'director',
                'movie': item['name']
            })

        for actor in item['actors']:
            actor_name = actor['name']
            actor_image = actor['image']
            yield Request(actor_image, meta={
                'name': actor_name,
                'type': 'actor',
                'movie': item['name']
            })
