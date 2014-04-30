__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class IteyesDemoCrawler(CrawlSpider):
    name = "iteye"
    allowed_domains = [
        "iteye.com"
    ]

    start_urls = [
        'http://www.cnblogs.com',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='^/.+/p/[0-9]+\.html$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'cnblogs'

        item['link'] = response.url

        item['content'] = sel.xpath('//a[@id="cb_post_title_url"]/text()')[0].extract()+ \
                          sel.xpath('//div[@id="article_content"]')[0].extract()

        return item