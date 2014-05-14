__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class CnblogsDemoCrawler(CrawlSpider):
    name = "cnblogs"
    allowed_domains = [
        "cnblogs.com"
    ]

    start_urls = [
        'http://www.cnblogs.com',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/.+/p/[0-9]+\.html$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        try:
            item['title'] = sel.xpath('//a[@id="cb_post_title_url"]/text()')[0].extract()
        except Exception:
            item['title'] = sel.xpath('//h1[@class="postTitle"]/text()')[0].extract()

        item['date'] = sel.xpath('//span[@id="post-date"]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-03

        item['fromsite'] = self.name

        item['link'] = response.url

        try:
            item['title'] = sel.xpath('//a[@id="cb_post_title_url"]/text()')[0].extract()
            try:
                item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()
            except Exception:
                item['content'] = sel.xpath('//div[@id="cnblogs_post_body"]')[0].extract()
        except Exception:
            item['title'] = sel.xpath('//h1[@class="postTitle"]/text()')[0].extract()
            item['content'] = sel.xpath('//div[@class="postBody"]')[0].extract()

        return item