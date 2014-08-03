__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request


class CnblogsDemoCrawler(CrawlSpider):
    name = "cnblogs"
    allowed_domains = [
        "cnblogs.com"
    ]

    start_urls = [
        'http://www.cnblogs.com',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="post_item_body"]/h3/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['date'] = sel.xpath('//span[@id="post-date"]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-03

        item['fromsite'] = self.name

        item['link'] = response.url

        try:
            item['title'] = sel.xpath('//a[@id="cb_post_title_url"]/text()')[0].extract()
            try:
                item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()
            except Exception:
                item['content'] = sel.xpath('//div[@id="cnblogs_post_body"]')[0].extract()
        except Exception:
            item['title'] = sel.xpath('//h1[@class="postTitle"]/text()')[0].extract()
            item['content'] = sel.xpath('//div[@class="postBody"]')[0].extract()

        item['tag'] = 'blogs'

        return item