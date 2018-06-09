# -*- coding: utf-8 -*-
import scrapy
import sys



class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['asheville.craigslist.org']
    start_urls = ['https://asheville.craigslist.org/search/sss'] 

    def parse(self, response):
        items_for_sale = response.xpath('//p[@class="result-info"]')
        
        for item in items_for_sale:
            title = item.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()
            date = item.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = item.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            price = item.xpath('.//span[@class="result-price"]/text()').extract_first()
            location = item.xpath('.//span[@class="result-hood"]/text()').extract_first()
            
            yield scrapy.Request(link,
                                 callback=self.parse_listing,
                                 meta={'Url': link,
                                       'Title': title,
                                       'Location': location,
                                       'Date': date,
                                       'Price': price})
            
        next_page_url = response.xpath('//a[text()="next > "]/@href').extract_first()
        if next_page_url:
          yield scrapy.Request('https://asheville.craigslist.org' + next_page_url, callback=self.parse)
            
            
    def parse_listing(self, response):
        title = response.meta['Title']
        location = response.meta['Location']
        date = response.meta['Date']
        link = response.meta['Url']
        price = response.meta['Price']
        condition = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        images = response.xpath('//*[@id="thumbs"]//@src').extract()
        images = [image.replace('50x50c', '600x450') for image in images]
        description = response.xpath('//*[@id="postingbody"]/text()').extract()

        try:
            latitude = response.xpath('//*[@id="map"]/@data-latitude').extract_first()
            longitude = response.xpath('//*[@id="map"]/@data-longitude').extract_first()
        except Exception:
            pass
        
        yield {'Title': title,
               'Price': price,
               'Location': location,
               'Date': date,
               'Url': link,
               'Condition': condition,
               'Images': images,
               'Description': description,
               'Latitude': latitude,
               'Longitude': longitude}
        
        
        
   