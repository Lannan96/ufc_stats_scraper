# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class UfcScraperItem(scrapy.Item):
    # define the fields for your item here like:
    fighter_id = Field()
    name = Field()
    height = Field()
    weight = Field()
    reach = Field()
    stance = Field()
    dob = Field()
    SLpM = Field()
    str_acc = Field()
    SApM = Field()
    str_def = Field()
    TD_avg = Field()
    TD_acc = Field()
    TD_def = Field()
    sub_avg = Field()

