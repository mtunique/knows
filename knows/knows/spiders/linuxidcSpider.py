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


class linuxidcSpider(CrawlSpider):
    name = 'linux'
    allowed_domains = ['linuxidc.com']

    start_urls = [
        'http://www.linuxidc.com/it/',
        'http://www.linuxidc.com/Linuxit/',
        'http://www.linuxidc.com/MySql/',
        'http://www.linuxidc.com/RedLinux/',
        'http://www.linuxidc.com/Apache/',
        'http://www.linuxidc.com/Unix/'
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="mm"]//div[@class="title"]//a/@href').extract():
            new_url = re.sub("\.\.", 'http://www.linuxidc.com', url)
            if judge_link(new_url):
                continue
            yield Request(new_url, callback="parse_article")

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="printBody"]//div[@id="content"]/p[2]')[0].extract()

        return item