# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StoryspiderItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    name = scrapy.Field()
    chapter = scrapy.Field()
    content = scrapy.Field()
