__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class ApkbusDemoCrawler(CrawlSpider):
    name = "apkbus"
    allowed_domains = [
        "apkbus.com"
    ]

    start_urls = [
        'http://www.apkbus.com',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='android-[0-9]+-1\.html$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'apkbus'

        item['link'] = response.url

        item['content'] = sel.xpath('//h1[@class="ph"]/text()')[0].extract()+\
                          sel.xpath('//td[@id="article_content"]')[0].extract()

        return item