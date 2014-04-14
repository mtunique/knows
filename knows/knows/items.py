from scrapy.item import Item, Field


class ArticleItem(Item):
    title = Field()
    date = Field()
    where = Field()
    content = Field()
