# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FzdmonepieceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    url_object = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    create_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
                        insert into fzdmonepiece(title, url, url_object, image_url, image_path, create_time)
                        VALUES(%s, %s, %s, %s, %s, %s)
                     '''

        params = (self['title'], self['url'], self['url_object'], self['image_url'], self['image_path'], self['create_time'])

        return insert_sql,params

    def get_query_sql(self):
        query_sql = """
                    select * from fzdmonepiece WHERE url_object='{0}'
                    """.self['url_object']
        return query_sql
