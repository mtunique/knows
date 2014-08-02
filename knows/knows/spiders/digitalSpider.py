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


class digitalSpider(CrawlSpider):
    name = "digitalTencent"
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
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//div[@class="hd"]/h1/text()')[0].extract()

        raw_date = sel.xpath('//span[@class="pubTime"]/text()')[0].extract()
        match_list = re.findall(r'([0-9]{2,4})', raw_date)
        #separate into [u'2014', u'05', u'10', u'07', u'51'], only need the first 3 elements
        real_date = '-'.join(match_list[0:3])
        item['date'] = real_date
        #date format:2014-05-06

        item['fromsite'] = self.name

        item['link'] = response.url

        raw_content = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]/p').extract()
        real_content = ""
        for str in raw_content:
            real_content = str + real_content

        item['content'] = real_content

        if 'yy.htm' in response.url:
            item['tag'] = 'appanalyze'
        else:
            item['tag'] = 'news'

        return item