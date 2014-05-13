__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links


class IteyesDemoCrawler(CrawlSpider):
    name = "iteye"
    allowed_domains = [
        "iteye.com"
    ]

    start_urls = [
        'http://www.iteye.com/blogs/category/mobile',
        'http://www.iteye.com/blogs/category/web',
        'http://www.iteye.com/blogs/category/architecture',
        'http://www.iteye.com/blogs/category/language',
        'http://www.iteye.com/blogs/category/internet',
        'http://www.iteye.com/blogs/category/opensource',
        'http://www.iteye.com/blogs/category/os',
        'http://www.iteye.com/blogs/category/database',
        'http://www.iteye.com/blogs/category/develop',
        'http://www.iteye.com/blogs/category/industry',
        'http://www.iteye.com/blogs/category/other',
        'http://www.iteye.com/news/category/mobile',
        'http://www.iteye.com/news/category/web',
        'http://www.iteye.com/news/category/architecture',
        'http://www.iteye.com/news/category/language',
        'http://www.iteye.com/news/category/internet',
        'http://www.iteye.com/news/category/opensource',
        'http://www.iteye.com/news/category/os',
        'http://www.iteye.com/news/category/database',
        'http://www.iteye.com/news/category/develop',
        'http://www.iteye.com/news/category/industry',
        'http://www.iteye.com/news/category/other',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow='/blog/[0-9]+$',), callback='parse_article_blog', process_links=process_links),
        Rule(SgmlLinkExtractor(allow='/news/[0-9]+[^#]$',), callback='parse_article_news', process_links=process_links)
    ]

    def parse_article_blog(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = self.name+'_blog'

        item['link'] = response.url

        item['content'] = sel.xpath('//h3/a')[0].extract()+ \
                          sel.xpath('//div[@id="blog_content"]')[0].extract()

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['fromsite'] = self.name+'_news'

        item['link'] = response.url

        item['content'] = sel.xpath('//a[@href="'+response.url[20:]+'"]')[0].extract()+ \
                          sel.xpath('//div[@id="news_content"]')[0].extract()

        return item