# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    video_id = scrapy.Field()
    video_name = scrapy.Field()
    video_aliasname = scrapy.Field()
    video_updateinfo = scrapy.Field()
    video_region = scrapy.Field()
    video_type = scrapy.Field()
    video_years = scrapy.Field()
    video_tag = scrapy.Field()
    video_index = scrapy.Field()
    video_desc = scrapy.Field()
    video_detailurl = scrapy.Field()
    video_episodeurl = scrapy.Field()
    video_picurl = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    

class VideoEpisodeItem(scrapy.Item):
    # define the fields for your item here like:
    video_id = scrapy.Field()
    episode_url = scrapy.Field()
    episode_name = scrapy.Field()
    
