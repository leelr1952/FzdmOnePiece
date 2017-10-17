# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest
import MySQLdb
import MySQLdb.cursors
from FzdmOnePiece.utils.common import get_md5


class FzdmonepieceSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua_type():
            return getattr(self.ua, self.ua_type)

        random_ua = get_ua_type()

        request.headers.setdefault("User-Agent", random_ua)


class JSPageMiddleware(object):
    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == 'fzdmop':
            print(request.url)
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问：{0}".format(request.url))

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")


class MysqlQueryMiddleware(object):
    # 每次请求查询数据库url_object，已存在则跳过
    def __init__(self):
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="leelr1952", db="fzdmop", charset="utf8")
        self.cursor = conn.cursor()

    def process_request(self, request, spider):
        query_sql_object = get_md5(request.url)
        if request.url != "http://manhua.fzdm.com/2/":
            query_sql = """
                           select * from fzdmonepiece WHERE url_object='{0}'
                        """.format(query_sql_object)
            # result = self.cursor.execute(query_sql)
            # for info in self.cursor.fetchall():
            #     if query_sql_object == info[2]:
            if self.cursor.execute(query_sql):
                print("IgnoreRequest : %s" % request.url)
                raise IgnoreRequest("IgnoreRequest : %s" % request.url)

            else:
                return None

