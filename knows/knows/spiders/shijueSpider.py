__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
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
        'http://shijue.me/difference/18/latest',
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

        item['title'] = sel.xpath('//span[@id="stuff_stick_img"]/text()')[0].extract()

        item['date'] = sel.xpath('//meta[@name="weibo: article:create_at"]/@content')[0].extract().split(' ')[0]
        #date format:2014-04-03

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="article-body mt-20"]')[0].extract()

        item['tag'] = 'Design'

        return item