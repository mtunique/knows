__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import judge_link
from scrapy.http import Request
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

    def parse_start_url(self, response):
        if response.url == 'http://www.oschina.net/blog':
            slp = Selector(response)
            for url in slp.xpath('//ul[@class="BlogList"]/li/div/h3/a/@href').extract():
                if not url.startswith('http'):
                    url = 'http://www.oschina.net/blog%s' % url
                if judge_link(url):
                    continue
                yield Request(url, callback=self.parse_article_blog)

        if response.url == 'http://www.oschina.net/news':
            slp = Selector(response)
            for url in slp.xpath('//ul[@class="List"]/li/h2/a/@href').extract():
                if not url.startswith('http'):
                    url = 'http://www.oschina.net/news%s' % url
                if judge_link(url):
                    continue
                yield Request(url, callback=self.parse_article_news)

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

        item['tag'] = 'blogs'

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h1[@class="OSCTitle"]/text()')[0].extract()

        raw_date = sel.xpath('//div[@class="PubDate"]/text()')[1].extract()
        raw_date_list = re.findall(r'[0-9]{2,4}', raw_date)
        item['date'] = '-'.join(raw_date_list)
        #date format:2014-05-11

        item['fromsite'] = self.name + '_news'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@class="Body NewsContent TextContent"]')[0].extract()

        item['tag'] = 'news'

        return item