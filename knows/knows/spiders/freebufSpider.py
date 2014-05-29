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
    name = "freebuf"
    allowed_domains = [
        "freebuf.com"
    ]

    start_urls = [
        'http://www.freebuf.com/news',
        'http://www.freebuf.com/tools',
        'http://www.freebuf.com/articles',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="news_inner"]/dl/dt/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article,)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//div[@class="news_tit"]/h3/text()')[0].extract()

        raw_date = sel.xpath('//div[@class="news_tit"]/p/text()')[1].extract()
        raw_date_list = re.findall(r'[0-9]{2,4}', raw_date)
        item['date'] = '-'.join(raw_date_list)
        #date format:2014-5-7

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="news_text"]')[0].extract()

        item['tag'] = 'Tech'

        return item