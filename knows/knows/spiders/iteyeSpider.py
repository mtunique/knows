__author__ = 'mt'
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from knows.items import ArticleItem
from baseFunctions import process_links
from baseFunctions import judge_link
from scrapy.http import Request


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

    def parse_start_url(self, response):
        slp = Selector(response)

        if "blogs" in response.url:
            url_list_blogs = slp.xpath('//div[@class="content"]/h3/a/@href').extract()

            for url in url_list_blogs:
                new_url_blogs = url
                if judge_link(new_url_blogs):
                    continue
                yield Request(new_url_blogs, callback=self.parse_article_blog)

        else:
            raw_url_list_news = slp.xpath('//div[@class="content"]/h3/a/@href').extract()

            for url in raw_url_list_news:
                new_url_news = "http://www.iteye.com" + url
                if judge_link(new_url_news):
                    continue
                yield Request(new_url_news, callback=self.parse_article_news)

    def parse_article_blog(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//h3/a/text()')[0].extract()

        item['date'] = sel.xpath('//div[@class="blog_bottom"]//li[1]/text()')[0].extract().split(' ')[0]
        #date format:2014-05-08
        #Attention:This blog page date format may be like "10小时前"
        #this error occurs everytime cause we always scrape the latest news from the site,
        # and all the latest news use this form of time, fuck them all this site we can use the time we scrape
        # instead of the article time given

        item['fromsite'] = self.name+'_blog'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="blog_content"]')[0].extract()

        item['tag'] = 'blogs'

        return item

    def parse_article_news(self, response):
        sel = Selector(response)

        item = ArticleItem()

        item['title'] = sel.xpath('//a[@href="'+response.url[20:]+'"]/text()')[0].extract()

        item['date'] = sel.xpath('//span[@class="date"]/text()')[0].extract().split(' ')[0]
        #date format:2014-04-22

        item['fromsite'] = self.name+'_news'

        item['link'] = response.url

        item['content'] = sel.xpath('//div[@id="news_content"]')[0].extract()

        item['tag'] = 'news'

        return item