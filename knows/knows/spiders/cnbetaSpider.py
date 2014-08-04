__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
from scrapy.spider import Spider
from baseFunctions import judge_link


class cnBetaSpider(CrawlSpider):
    name = "cnbeta"
    allowed_domains = ["cnbeta.com"]
    start_urls = [
        "http://www.cnbeta.com/"
    ]

    def parse(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="items_area"]/dl/dt/a/@href').extract():
            new_url = "http://www.cnbeta.com" + url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['content'] = sel.xpath('//div[@class="content"]')[0].extract()

        item['fromsite'] = self.name

        item['link'] = response.url

        item['date'] = sel.xpath('//span[@class="date"]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-07

        item['title'] = sel.xpath('//div[@class="body"]/header/h2/text()')[0].extract()

        item['tag'] = 'news'

        return item
