__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class OschinaDemoCrawler(CrawlSpider):
    name = "oschina"
    allowed_domains = [
        "oschina.net"
    ]

    start_urls = [
        'http://www.oschina.net/blog',
        'http://www.oschina.net/news'
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/.+/blog/[0-9]+$',), callback='parse_article_blog', process_links=process_links),
        Rule(SgmlLinkExtractor(allow='/news/[0-9]+/.+$',), callback='parse_article_news', process_links=process_links)
    ]

    def parse_article_blog(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'oschina_blog'

        item['link'] = response.url

        item['content'] =sel.xpath('//div[@class="BlogTitle"]/h1')[0].extract()\
                         + sel.xpath('//div[@class="BlogContent"]')[0].extract()

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'oschina_news'

        item['link'] = response.url

        item['content'] =sel.xpath('//h1[@class="OSCTitle"]/text()')[0].extract()\
                         +sel.xpath('//div[@class="Body NewsContent TextContent"]')[0].extract()

        return item