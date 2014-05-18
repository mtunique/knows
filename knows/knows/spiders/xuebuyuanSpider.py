__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links, judge_link
import re


class XuebuyuanDemoCrawler(CrawlSpider):
    name = "xuebuyuan"
    allowed_domains = [
        "xuebuyuan.com"
    ]

    start_urls = [
        'http://www.xuebuyuan.com/category/web%E5%89%8D%E7%AB%AF',
        'http://www.xuebuyuan.com/category/%E6%95%B0%E6%8D%AE%E5%BA%93',
        'http://www.xuebuyuan.com/category/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80',
        'http://www.xuebuyuan.com/category/%E6%90%9C%E7%B4%A2%E6%8A%80%E6%9C%AF',
        'http://www.xuebuyuan.com/category/%E7%AE%97%E6%B3%95',
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//span[@class="archive_more"]/a/@href').extract():
            new_url = url
            if judge_link(new_url):
               continue
            yield Request(new_url, callback="parse_article")


    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h2[@class="entry_title"]/text()')[0].extract()

        raw_date = sel.xpath('//span[@class="date"]/text()')[0].extract()
        raw_date_list = re.findall(r'[0-9]{2,4}', raw_date)
        item['date'] = '-'.join(raw_date_list)
        #date format:2014-04-10

        item['fromsite'] = self.name

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="article_content"]')[0].extract()

        item['tag'] = 'Tech'

        return item