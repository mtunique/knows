__author__ = 'M.X'
# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
import re


class IfanrDemoCrawler(CrawlSpider):
    name = "itpub"
    allowed_domains = [
        "itpub.net"
    ]

    start_urls = [
        'http://blog.itpub.net/site/index/',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="classify_con1"]/div[@class="two_cont2_1"]/a/@href').extract():
            new_url = "http://blog.itpub.net" + url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article,)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//div[@class="Blog_tit4 Blog_tit5"]/a/text()')[0].extract()

        item['date'] = sel.xpath('//div[@class="Blog_tit4 Blog_tit5"]/em/text()')[0].extract().split(' ')[0]
        #date format:2014-05-07

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="Blog_wz1"]/span[1]')[0].extract()

        item['tag'] = 'Tech'

        return item