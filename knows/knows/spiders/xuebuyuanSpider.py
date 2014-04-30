__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class CsdnDemoCrawler(CrawlSpider):
    name = "xuebuyuan"
    allowed_domains = [
        "xuebuyuan.com"
    ]

    start_urls = [
        'http://www.xuebuyuan.com',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='^/[0-9]+\.html$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'xuebuyuan'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()

        return item