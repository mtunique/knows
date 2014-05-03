__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from many_crawler_set.items import ArticleItem
from scrapy.spider import BaseSpider
from baseFunctions import judge_link
import re


class uisdcSpider(CrawlSpider):
    name = "uisdc"
    allowed_domains = ['uisdc.com']

    start_urls = [
        'http://www.uisdc.com/archives/page/1',
        'http://www.uisdc.com/archives/page/2',
        'http://www.uisdc.com/archives/page/3',
        'http://www.uisdc.com/archives/page/4',
        'http://www.uisdc.com/archives/page/5',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="hfeed"]/div/a[1]/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback="parse_article")

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="entry-content"]')[0].extract()

        return item