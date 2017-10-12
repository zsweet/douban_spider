# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CqcDoubanItem(scrapy.Item):
    collection = 'movies_copy'
    id = Field()
    actors = Field()
    director = Field()
    country = Field()
    dateCountry = Field()
    language = Field()
    duration = Field()
    imdb = Field()
    kind = Field()
    comments = Field()
    reviews = Field()
    screenwriter = Field()
    rating = Field()
    rating_sum = Field()
    rating_per = Field()
    rating_betterthan = Field()
    nickname = Field()

