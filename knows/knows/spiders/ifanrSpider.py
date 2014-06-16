__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request


class IfanrDemoCrawler(CrawlSpider):
    name = "ifanr"
    allowed_domains = [
        "ifanr.com"
    ]

    start_urls = [
        'http://www.ifanr.com/category/special/smarthome',
        'http://www.ifanr.com/category/special/opinion',
        'http://www.ifanr.com/category/special/company',
        'http://www.ifanr.com/category/special/device',
        'http://www.ifanr.com/category/special/people',
        'http://www.ifanr.com/category/special/health-special',
        'http://www.ifanr.com/category/special/intelligentcar',
        'http://www.ifanr.com/category/special/pattern',
        'http://www.ifanr.com/category/special/app-special',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//h2[@class="entry-name yahei"]/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//div[@class="entry-header"]/h1/a/text()')[0].extract()

        item['date'] = sel.xpath('//meta[@name="weibo: article:create_at"]/@content')[0].extract().split(' ')[0]
        #date format:2014-05-08

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="entry-content"]')[0].extract()

        item['tag'] = 'news'

        return item