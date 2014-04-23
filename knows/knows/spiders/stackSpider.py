__author__ = 'M.X'
# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class StackDemoSpider(CrawlSpider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://www.stackoverflow.com/questions?sort=frequent"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='questions/[0-9]{1,}/'), callback="parse_stack_urls", process_links=process_links)
    ]

    def parse_stack_urls(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//head/meta[@name="og:title"]/@content')[0].extract()

        item['fromsite'] = 'Stack OverFLow'

        item['link'] = response.url

        item['date'] = sel.xpath('//div[@class="question"]/table//div[@class="user-action-time"]//span/@title')[0].extract()

        #seq1 = question explaination <----> seq2 = best voted answer
        seq1 = sel.xpath('//div[@class="question"]/table//div[@class="post-text"]')[0].extract()
        seq2 = sel.xpath('//div[@id="answers"]//div[@data-answerid][1]//div[@class="post-text"]')[0].extract()
        item['content'] = '<p>qusetion:</p>'+seq1.decode('utf-8')+'</br><p>best answer:</p>'+seq2.decode('utf-8')

        return item