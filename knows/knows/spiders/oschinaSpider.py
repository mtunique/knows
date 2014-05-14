__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links
import re


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

        item['title'] = sel.xpath('//div[@class="BlogTitle"]/h1/text()')[0].extract()

        raw_date = sel.xpath('//div[@class="BlogTitle"]/div[@class="BlogStat"]/text()')[0].extract()
        pattern = re.compile(r'\((.*?)\)', re.I)
        match_date = pattern.findall(raw_date)
        item['date'] = match_date[0].split(' ')[0]
        #date format:2014-05-11

        item['fromsite'] = self.name + '_blog'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="BlogContent"]')[0].extract()

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h1[@class="OSCTitle"]/text()')[0].extract()

        raw_date = sel.xpath('//div[@class="PubDate"]/text()')[1].extract()
        raw_date_list = re.findall(r'[0-9]{2,4}', str)
        item['date'] = '-'.join(raw_date_list)
        #date format:2014-05-11

        item['fromsite'] = self.name + '_news'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="Body NewsContent TextContent"]')[0].extract()

        return item