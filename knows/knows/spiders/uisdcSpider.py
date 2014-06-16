__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
from baseFunctions import judge_link
import re


class uisdcSpider(CrawlSpider):
    name = "uisdc"
    allowed_domains = ['uisdc.com']

    start_urls = [
        'http://www.uisdc.com/archives/page/1'
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="hfeed index-feed"]/div/a[1]/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h1[@class="post-title entry-title"]/text()')[0].extract()

        raw_date = sel.xpath('//abbr[@class="published"]/text()')[0].extract()
        item['date'] = re.sub('/', '-', raw_date)
        #date format:2014-5-6

        item['fromsite'] = self.name

        item['link'] = response.url

        raw_content = sel.xpath('//div[@class="entry-content"]/*[position()<(last()-3)]').extract()
        real_content = ''
        for line in raw_content:
            real_content = real_content + line
        item['content'] = real_content

        item['tag'] = 'Design'

        return item