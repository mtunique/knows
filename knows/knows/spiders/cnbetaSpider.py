__author__ = 'M.X'

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from knows.items import ArticleItem
from scrapy.spider import BaseSpider


class cnBetaSpider(BaseSpider):
    name = "cnbeta1"
    allowed_domains = ["cnbeta.com"]
    start_urls = [
        "http://www.cnbeta.com/"
    ]

    def parse(self, response):
        slp = Selector(response)

        for url in slp.xpath('//div[@class="items_area"]/dl/dt/a/@href').extract():
            new_url = "http://www.cnbeta.com" + url
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['content'] = sel.xpath('//div[@class="content"]').extract()

        item['sitename'] = 'cnBeta'

        item['where'] = response.url

        item['date'] = sel.xpath('//span[@class="date"]/text()').extract()

        item['title'] = sel.xpath('//div[@class="body"]/header/h2/text()').extract()

        return item
