# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionAnswersParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HeaderItem(scrapy.Item):
    question = scrapy.Field()
    answer = scrapy.Field()
    length = scrapy.Field()
    