from scrapy.item import Item, Field


class ArticleItem(Item):
    #taken from which website
    fromsite = Field()
    date = Field()
    title = Field()
    #link to the article
    where = Field()
    #short summery of the article
    desc = Field()

    content = Field()
    #----------------------------------------
    #the following are items specially used for Q&A platform
    #----------------------------------------
    problem = Field()
    solution = Field()