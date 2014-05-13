__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class IfanrDemoCrawler(CrawlSpider):
    name = "coolshell"
    allowed_domains = [
        "coolshell.cn"
    ]

    start_urls = [
        'http://www.coolshell.cn',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/articles/[0-9]+\.html$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="post"]/h2')[0].extract()+\
                          sel.xpath('//div[@class="post"]/div[@class="content"]')[0].extract()

        return item