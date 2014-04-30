# Scrapy settings for spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'knows'

SPIDER_MODULES = ['knows.spiders']
NEWSPIDER_MODULE = 'knows.spiders'

ITEM_PIPELINES = {'knows.pipelines.ArticleInsertPipeline': 1,
}

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider (+http://www.yourdomain.com)'
