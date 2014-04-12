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

ITEM_PIPELINES = {'knows.pipelines.ArticleInsertPipline': 1,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider (+http://www.yourdomain.com)'
