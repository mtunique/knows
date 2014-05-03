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


class digitalSpider(CrawlSpider):
    name = "digital"
    allowed_domains = ["qq.com"]

    start_urls = [
        'http://digi.tech.qq.com/dn.htm',
        'http://digi.tech.qq.com/pb.htm',
        'http://digi.tech.qq.com/yx.htm',
        'http://digi.tech.qq.com/yy.htm',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@id="listZone"]//div[@class="Q-tpList"]/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback="parse_article")

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['link'] = response.url

        raw_content = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]/p').extract()
        for str in raw_content:
            real_content = str + real_content

        item['content'] = real_content

        return item