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
            yield Request(new_url, callback="parse_article")

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()

        return item