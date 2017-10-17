import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、解析列表页中文章的url并交给scrapy下载并解析
        2、获取下一页url交给scrapy下载，下载完成后交给parse
        """

        # 解析列表页中文章的url并交给scrapy下载并解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        # 提取下一页交给scrapy
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse)

    def parse_detail(self,response):
        # article_item = JobBoleArticleItem()

        # 通过css选择器定位字段
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图获取
        title_css = response.css(".entry-header h1::text").extract()[0]
        create_date_css = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·","")
        praise_nums_css = int(response.css('.vote-post-up h10::text').extract()[0])
        fav_nums_css = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums_css)
        if match_re:
            fav_nums_css = int(match_re.group(1))
        else:
            fav_nums_css = 0

        comment_nums_css = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums_css)
        if match_re:
            comment_nums_css = int(match_re.group(1))
        else:
            comment_nums_css = 0

        content_css = response.css('.entry').extract()[0]

        tag_list_css = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag_list_css = [element for element in tag_list_css if not element.strip().endswith(u"评论")]
        tags_css = ",".join(tag_list_css)

        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['title'] = title_css
        # try:
        #     create_date_css = datetime.datetime.strptime(create_date_css, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date_css = datetime.datetime.now().date()
        # article_item['create_date'] = create_date_css
        # article_item['url'] = response.url
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums_css
        # article_item['comment_nums'] = comment_nums_css
        # article_item['fav_nums'] = fav_nums_css
        # article_item['tags'] = tags_css
        # article_item['content'] = content_css

        # 调用itemloader处理
        # item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_css("title", ".entry-header h1::text")
        # item_loader.add_value("url", response.url)
        # item_loader.add_value('url_object_id', get_md5(response.url))
        # item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        # item_loader.add_value('front_image_url', [front_image_url])
        # item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        # item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        # item_loader.add_css('fav_nums', '.bookmark-btn::text')
        # item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        # item_loader.add_css('content', '.entry')
        #
        # article_item = item_loader.load_item()
        #
        # yield article_item