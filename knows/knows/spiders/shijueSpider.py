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


class shijueSpider(CrawlSpider):
    name = 'shijue'
    allowed_domains = ['shijue.me']

    start_urls = [
        'http://shijue.me/news/13/latest',
        'http://shijue.me/news/14/latest',
        'http://shijue.me/news/15/latest',
        'http://shijue.me/difference/17/latest',
        'http://shijue.me/news/19/latest',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="masonry-box"]//div[@class="thumbnail bbox"]/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback="parse_article")

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="article-body mt-20"]')[0].extract()

        return item