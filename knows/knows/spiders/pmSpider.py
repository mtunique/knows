__author__ = 'M.X'
# -*- coding: UTF-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
from scrapy.spider import BaseSpider
from baseFunctions import judge_link
import re


class pmSpider(CrawlSpider):
    name = "woshipm"
    allowed_domains = ["woshipm.com"]

    start_urls = [
        'http://www.woshipm.com/category/pmd',
        'http://www.woshipm.com/category/it',
        'http://www.woshipm.com/category/operate',
        'http://www.woshipm.com/category/zhichang',
        'http://www.woshipm.com/category/pd',
        'http://www.woshipm.com/category/ucd'
    ]

    def parse_start_url(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="content_box bor_cor"]//div[@class="f_img_box"]/a/@href').extract():
            new_url = url
            if judge_link(new_url):
                continue
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//div[@class="con_title"]/h1/text()')[0].extract()

        item['date'] = sel.xpath('//span[@class="con_t_time"]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-06

        item['fromsite'] = self.name

        item['link'] = response.url

        raw_content = sel.xpath('//div[@class="con_txt clx"]/*[position()<(last()-1)]').extract()
        real_content = ''
        for str in raw_content:
            real_content = str + real_content
        item['content'] = real_content

        item['tag'] = 'PM&APP'

        return item
