__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request


class CsdnDemoCrawler(CrawlSpider):
    name = "csdn"
    allowed_domains = [
        "csdn.net"
    ]

    start_urls = [
        'http://news.csdn.net/news/1',
        'http://mobile.csdn.net/mobile/1',
        'http://cloud.csdn.net/cloud/1',
        'http://sd.csdn.net/sd/1',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="unit"]/h1/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h1[@class="title"]/text()')[0].extract()

        item['date'] = response.url.split('/')[4]
        #date format:2014-05-07

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="con news_content"]')[0].extract()

        return item

    # def parse_article_news(self, response):
    #     sel = Selector(response)
    #
    #     item = ArticleItem()
    #
    #     item['title'] = sel.xpath('//h1/text()')[0].extract()
    #
    #     raw_date = sel.xpath('//ul[@class="pull-left"]/li[1]/text()')[0].extract()
    #     item['date'] = raw_date[1:11]
    #     #date format:2014-05-07
    #
    #     item['fromsite'] = self.name
    #
    #     item['link'] = response.url
    #
    #     item['content'] = sel.xpath('//div[@class="content document_file_content"]')[0].extract()
    #
    #     item['tag'] = 'news'
    #
    #
    #     return item