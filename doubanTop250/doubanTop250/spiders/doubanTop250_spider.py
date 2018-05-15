#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from doubanTop250.items import Doubantop250Item

class Doubantop250Spider(scrapy.Spider):
    """docstring for DoubanTop250Spider"""
    name = 'doubanTop250'
    allowed_domains = ["douban.com"]
    start_urls = [
        "https://movie.douban.com/top250"
    ]

    def parse(self, response):
        for info in response.xpath('//div[@class="item"]'):
            item = Doubantop250Item()
            item["rank"] = info.xpath('div[@class="pic"]/em/text()').extract()
            item["title"] = info.xpath('div[@class="pic"]/a/img/@alt').extract()
            item["link"] = info.xpath('div[@class="pic"]/a/@href').extract()
            item["star"] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            item["rate"] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').extract()
            item["quote"] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            yield item

        # 翻页
        next_page = response.xpath('//span[@class="next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
