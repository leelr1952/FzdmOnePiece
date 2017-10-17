import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from FzdmOnePiece.items import FzdmonepieceItem
from FzdmOnePiece.settings import SQL_DATETIME_FORMAT
from FzdmOnePiece.utils.common import get_md5


class FzdmopSpider(scrapy.Spider):
    name = 'fzdmop'
    allowed_domains = ['manhua.fzdm.com']
    start_urls = ['http://manhua.fzdm.com/2/']

    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/" \
            "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

    header = {
        "User-Agent": agent,
    }

    def parse(self, response):
        """
        This is fzdm onepiece menu,post_nodes is the every li->a element.
        :param response:
        :return: parse the detail page,yield
        """
        post_nodes = response.css('#content .pure-u-1-2 a')
        for node in post_nodes:
            node_title = node.css('::attr(title)').extract_first("")
            node_url = node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, node_url), meta={'title': node_title,'node_url':node_url},
                          callback=self.parse_detail, headers=self.header)

    def parse_detail(self,response):
        """
        Get the onepiece picture
        :param response:
        :return:
        """
        fzdmopitem = FzdmonepieceItem()
        title = response.meta.get('title', '')
        node_url = response.meta.get('node_url','')

        match_img_src = re.match('.*var mhurl = "(.*?)"', response.text, re.DOTALL)
        match_img_host = re.match('.*mhss = "(.*?)"', response.text, re.DOTALL)
        match_next_image_url = re.match(".*<a href='(.*?)'.*下一页", response.text, re.DOTALL)

        if match_img_src and match_img_host:
            img_src = "http://" + match_img_host.group(1) + "/" + match_img_src.group(1)
            print(img_src)
        else:
            print("no pic")
        if match_next_image_url:
            print(match_next_image_url.group(1))
            next_image_url = "http://manhua.fzdm.com/2/" + node_url + match_next_image_url.group(1)
            yield Request(url=next_image_url, callback=self.parse_detail,
                          meta={'title': title,'node_url':node_url}, headers=self.header)

        fzdmopitem['title'] = title
        fzdmopitem['url'] = response.url
        fzdmopitem['url_object'] = get_md5(response.url)
        # fzdmopitem['image_url'] = [img_src]   imagepipeline时使用
        fzdmopitem['image_url'] = img_src
        # fzdmopitem['create_time'] = datetime.datetime.now()
        fzdmopitem['create_time'] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        yield fzdmopitem
