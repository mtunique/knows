__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request

class CsdnDemoCrawler(CrawlSpider):
    name = "csdn_blog"
    allowed_domains = [
        "csdn.net"
    ]

    start_urls = [
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
        'http://blog.csdn.net/mobile/newest.html',
        'http://blog.csdn.net/web/newest.html',
        'http://blog.csdn.net/enterprise/newest.html',
        'http://blog.csdn.net/code/newest.html',
        'http://blog.csdn.net/www/newest.html',
        'http://blog.csdn.net/database/newest.html',
        'http://blog.csdn.net/system/newest.html',
        'http://blog.csdn.net/cloud/newest.html',
        'http://blog.csdn.net/software/newest.html',
        'http://blog.csdn.net/other/newest.html',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="blog_list"]/h1/a[@name]/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//span[@class="link_title"]/a/text()')[0].extract()

        item['date'] = sel.xpath('//span[@class="link_postdate"]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-07

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()

        item['tag'] = 'blogs'

        return item