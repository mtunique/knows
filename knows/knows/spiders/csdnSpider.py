__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class CsdnDemoCrawler(CrawlSpider):
    name = "csdn"
    allowed_domains = [
        "csdn.net"
    ]

    start_urls = [
        'http://www.csdn.net/rollingnews.html',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/article/[^t]+/.*$',), callback='parse_article', process_links=process_links),
        Rule(SgmlLinkExtractor(allow='/news/.*$',), callback='parse_article_news', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'csdn'

        item['link'] = response.url

        item['content'] = sel.xpath('//h1[@class="title"]')[0].extract() \
                          +sel.xpath('//div[@class="con news_content"]')[0].extract()

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//h1')[0].extract()+\
                          sel.xpath('//div[@class="content document_file_content"]')[0].extract()


        return item