from scrapy.item import Item, Field


class ArticleItem(Item):
    #taken from which website
    fromsite = Field()
    date = Field()
    title = Field()
    #link to the article
    link = Field()
    #when it's an article,it contains the content&pics
    #when it's a question&answer, it contains the best one
    content = Field()