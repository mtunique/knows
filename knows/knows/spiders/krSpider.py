__author__ = 'M.X'

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class KrDemoCrawler(CrawlSpider):
    name = "kr"
    allowed_domains = [
        "36kr.com"
    ]

    start_urls = [
        "http://www.36kr.com/topic/technology"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/p/[0-9]{6}',), callback='parse_article', process_links=process_links)
    ]

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//header[@class="single-post-header__meta"]//h1/text()')[0].extract()

        lst = sel.xpath('//header[@class="single-post-header__meta"]/div/text()').extract()[0].split(' ')
        p = lst[2] + ',' + lst[3]
        #q = []
        item['date'] = p

        item['fromsite'] = '36Kr'

        item['link'] = response.url

        item['content'] = sel.xpath('//section[@class="article"]')[0].extract()

        return item