__author__ = 'M.X'

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem


class KrDemoCrawler(CrawlSpider):
    name = "kr"
    allowed_domains = [
        "36kr.com"
    ]

    start_urls = [
        "http://www.36kr.com/topic/technology"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/p/[0-9]{6}',), callback='parse_article')
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//header[@class="single-post-header__meta"]//h1/text()').extract()

        lst = sel.xpath('//header[@class="single-post-header__meta"]/div/text()').extract()[0].split(' ')
        p = lst[2] + ',' + lst[3]
        #q = []
        item['date'] = p

        item['sitename'] = '36Kr'

        item['where'] = sel.xpath('//head/meta[@name="twitter:url"]/@content').extract()

        item['content'] = sel.xpath('//section[@class="article"]').extract()

        return item