__author__ = 'mt'
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
import re


class GroupTestSpider(CrawlSpider):
    name = "cnbeta"
    allowed_domains = ["cnbeta.com"]
    start_urls = [
            "http://www.cnbeta.com/"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=('/articles/\d+?.htm$', )), callback='parse_article', follow=True),
        ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()
        item['content'] = sel.xpath('//div[@class="content"]')[0].extract()
        return item