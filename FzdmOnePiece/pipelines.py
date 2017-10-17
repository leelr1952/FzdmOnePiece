# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
import os
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class FzdmonepiecePipeline(object):
    def process_item(self, item, spider):
        file_name = "%s_%s" % (item['title'], item['image_url'].split('/')[-1])  # 拼接文件名，学校_姓名
        dir_path = "D:\\FzdmOnePiece\\OnePiece\\%s" % item['title']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, file_name)  # 拼接这个图片的路径，我是放在F盘的pics文件夹下
        # if not os.path.exists(file_path):
        item['image_path'] = file_path
        urllib.request.urlretrieve(item['image_url'], file_path)  # 接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径

        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步操作异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同item构建不同的插入语句，并插入到mysql

        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class FzdmonepieceImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'onepiece/%s' % (image_guid)

    def item_completed(self, results, item, info):
        if 'image_url' in item:
            for ok,value in results:
                image_file_path = value['path']
            item['image_path'] = image_file_path

        return item