__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request


class ApkbusDemoCrawler(CrawlSpider):
    name = "apkbus"
    allowed_domains = [
        "apkbus.com"
    ]

    start_urls = [
        'http://www.apkbus.com',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        #bug fixed: class cl is everywhere so use a specific id attr to find it
        for url in slp.xpath('//div[@id="portal_block_711_content"]//dl[@class="cl"]/dt/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h1[@class="ph"]/text()')[0].extract()

        item['date'] = sel.xpath('//p[@class="xg1"]/text()')[0].extract().split(' ')[0].split('\n')[1]
        #date format:2014-5-9

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//td[@id="article_content"]')[0].extract()

        item['tag'] = 'Android'

        return item