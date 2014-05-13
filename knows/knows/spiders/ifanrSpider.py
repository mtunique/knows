__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class IfanrDemoCrawler(CrawlSpider):
    name = "ifanr"
    allowed_domains = [
        "ifanr.com"
    ]

    start_urls = [
        'http://www.ifanr.com',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='http://www.ifanr.com/[0-9]+$|/news/[0-9]+$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="entry-header"]/h1/a')[0].extract()+\
                          sel.xpath('//div[@class="entry-content"]')[0].extract()

        return item