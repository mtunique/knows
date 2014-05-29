__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links
from baseFunctions import judge_link


class KrDemoCrawler(CrawlSpider):
    name = "kr"
    allowed_domains = [
        "36kr.com"
    ]

    start_urls = [
        "http://www.36kr.com/topic/technology"
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//article[@class="posts post-1 cf"]//div[@class="meta"]/a/@href').extract():
            new_url = 'http://www.36kr.com' + url

            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//header[@class="single-post-header__meta"]//h1/text()')[0].extract()

        item['date'] = sel.xpath('//meta[@name="weibo: article:create_at"]/@content')[0].extract().split(' ')[0]
        #date format:2014-05-04

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//section[@class="article"]')[0].extract()

        item['tag'] = 'news'

        return item