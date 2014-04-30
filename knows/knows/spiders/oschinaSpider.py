__author__ = 'mt'
# -*- coding: utf-8 -*-
__author__ = 'M.X'

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class CsdnDemoCrawler(CrawlSpider):
    name = "oschina"
    allowed_domains = [
        "oschina.net"
    ]

    start_urls = [
        'http://www.oschina.net/blog',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/.+/blog/[0-9]+$',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'oschina'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="BlogContent"]')[0].extract()

        return item