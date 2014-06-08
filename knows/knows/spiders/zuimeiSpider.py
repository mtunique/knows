__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
from scrapy.spider import BaseSpider
from baseFunctions import judge_link
import re


class zuimeiSpider(CrawlSpider):
    name = "zuimei"
    allowed_domains = ["zuimeia.com"]

    start_urls = [
        'http://zuimeia.com/apps/?platform=1',
        'http://zuimeia.com/apps/?platform=2',
        'http://zuimeia.com/apps/?platform=3'
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="left-side"]/article/section//a[@class="article-img"]/@href').extract():
            new_url = "http://zuimeia.com" + url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        app_name = sel.xpath('//div[@class="app-title"]/h1/text()')[0].extract()
        appdesc_list = sel.xpath('//div[@class="app-title"]/h1/span/text()').extract()
        app_desc = appdesc_list[0] + appdesc_list[1]

        item['title'] = app_name + app_desc

        item['date'] = sel.xpath('//li[@class="pub-time"]/text()')[0].extract()
        #date format:2014-5-6

        item['fromsite'] = self.name

        item['link'] = response.url

        short_desc = '<p>' + sel.xpath('//div[@class="short-des"]/text()')[0].extract() + '</p>'
        item['content'] = short_desc + sel.xpath('//div[@id="article_content"]')[0].extract()

        item['tag'] = 'PM&APP'

        return item