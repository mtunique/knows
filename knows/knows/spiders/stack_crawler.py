__author__ = 'M.X'

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem


class StackDemoSpider(CrawlSpider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://www.stackoverflow.com/questions?sort=frequent"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='questions/[0-9]{1,}/'), callback="parse_stack_urls")
    ]

    def parse_stack_urls(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//head/meta[@name="og:title"]/@content').extract()

        item['fromsite'] = 'Stack OverFLow'

        item['link'] = response.url

        item['date'] = sel.xpath('//div[@class="question"]/table//div[@class="user-action-time"]//span/@title').extract()[0]

        #seq1 = question explaination <----> seq2 = best voted answer
        seq1 = sel.xpath('//div[@class="question"]/table//div[@class="post-text"]').extract()
        seq2 = sel.xpath('//div[@id="answers"]//div[@data-answerid][1]//div[@class="post-text"]').extract()
        item['content'] = seq1+seq2

        return item