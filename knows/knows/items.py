from scrapy.item import Item, Field


class ArticleItem(Item):
    #taken from which website
    fromsite = Field()
    date = Field()
    title = Field()
    #link to the article
    link = Field()
    #when it's an article,it contains the content&pics
    content = Field()
    #tags according to websites
    tag = Field()
