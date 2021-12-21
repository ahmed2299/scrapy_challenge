import re

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line
        area_urls = response.css('.test-inline a::attr(href)').getall()
        for area_url in area_urls:
            yield Request(url='https://londonrelocation.com'+area_url,
                          callback=self.parse_homes)


    def parse_homes(self,response):
        title=response.css('.bn-box_pd h1::text').get()
        price=response.css('.bn-box_pd h3::text').get()
        price=re.search(r"\d+",price)[0]

        # an example for adding a property to the json list:
        property = ItemLoader(item=Property())
        property.add_value('title', title)
        property.add_value('price', price) # 420 per week
        property.add_value('url', response.url)
        return property.load_item()
