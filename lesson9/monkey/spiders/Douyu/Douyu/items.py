# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 主播名称
    nickname = scrapy.Field()

    # 图片链接 
    imagelink = scrapy.Field()
