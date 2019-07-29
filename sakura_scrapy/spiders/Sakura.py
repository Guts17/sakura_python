# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import VideoItem

class SakuraSpider(scrapy.Spider):
    name = 'Sakura'
    allowed_domains = ['imomoe.io']
    start_urls = ['http://www.imomoe.io/so.asp']

    # 视频列表页面解析
    def parse(self, response):

        # 提取视频链接
        le = LinkExtractor(restrict_xpaths='//div[@class="fire l"]//div[@class="pics"]//li')
        links = le.extract_links(response)
        if links:
            for link in links:
                yield scrapy.Request(link.url, callback=self.parse_video)

        # 提取下一页链接
        """ le = LinkExtractor(restrict_xpaths="//div[@class='pages']//a[1]")
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse) """

        next_url = response.xpath("//div[@class='pages']//a[last()-1]//@href").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    # 视频详情页面解析
    def parse_video(self, response):
        baseurl = response.url
        endurl = baseurl.split('/')[-1]
        videoitem = VideoItem()
        videoitem['video_id'] = endurl.split('.')[0]
        videoitem['video_name'] = response.xpath('//div[@class="spay"]/a/text()').extract_first()
        videoitem['video_aliasname'] = response.xpath('//div[@class="alex"]//p[1]/text()').extract_first()
        videoitem['video_updateinfo'] = response.xpath('//div[@class="alex"]//p[2]/text()').extract_first()
        videoitem['video_region'] = response.xpath('//div[@class="alex"]//span[1]/a/text()').extract_first()
        videoitem['video_type'] = ','.join(response.xpath('//div[@class="alex"]//span[2]/a/text()').extract())
        videoitem['video_years'] = response.xpath('//div[@class="alex"]//span[3]/a/text()').extract_first()
        videoitem['video_tag'] = ','.join(response.xpath('//div[@class="alex"]//span[4]/a/text()').extract())
        videoitem['video_index'] = response.xpath('//div[@class="alex"]//span[5]/a/text()').extract_first()
        videoitem['video_desc'] = response.xpath('//div[@class="info"]/text()').extract_first()
        videoitem['video_detailurl'] = baseurl
        videoitem['video_picurl'] = response.xpath('//div[@class="tpic l"]/img/@src').extract_first()
        videoitem['image_urls'] = [videoitem['video_picurl']]

        first_episodeUrl = response.xpath('//div[@class="movurl"]//li//a//@href').extract_first()
        first_episodeUrl = response.urljoin(first_episodeUrl)
        request1 = scrapy.Request(first_episodeUrl, callback=self.parse_episodes)
        request1.meta["videoitem"] = videoitem
        yield request1  

        # yield videoitem

    def parse_episodes(self, response):
        videoitem = response.meta["videoitem"]
        videoitem["video_episodeurl"] = response.urljoin(response.xpath('//div[@class="player"]/script[1]/@src').extract_first())
        yield videoitem
