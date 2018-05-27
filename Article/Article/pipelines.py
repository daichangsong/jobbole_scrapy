# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb


class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义 json 文件导出
    def __init__(self):
       self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', password='Alves123', db='scrapyspider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # insert_sql = """
        #     INSERT INTO jobbole_article(
        #       title, url, create_date, favor_nums, url_object_id,
        #       comment_nums, praise_nums, content, author, tags)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """
        # self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['favor_nums'],
        #                     item['url_object_id'], item['comment_nums'], item['praise_nums'],
        #                     item['content'], item['author'], item['tags']))
        insert_sql = """
            INSERT INTO jobbole_article(title, url, create_date, favor_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['favor_nums']))
        self.conn.commit()
