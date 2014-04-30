__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class CsdnDemoCrawler(CrawlSpider):
    name = "csdn"
    allowed_domains = [
        "csdn.net"
    ]

    start_urls = [
        'http://blog.csdn.net/',
        'http://blog.csdn.net/mobile/index.html',
        'http://blog.csdn.net/web/index.html',
        'http://blog.csdn.net/enterprise/index.html',
        'http://blog.csdn.net/code/index.html',
        'http://blog.csdn.net/www/index.html',
        'http://blog.csdn.net/database/index.html',
        'http://blog.csdn.net/system/index.html',
        'http://blog.csdn.net/cloud/index.html',
        'http://blog.csdn.net/software/index.html',
        'http://blog.csdn.net/other/index.html',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/.+/article/details/[0-9]{8}',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = 'csdn'

        item['link'] = response.url

        item['content'] = sel.xpath('//span[@class="link_title"]')[0].extract() \
                          +sel.xpath('//div[@id="article_content"]')[0].extract()

        return item