# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import re
from time import sleep

class LetgoSpider(scrapy.Spider):
    name = 'letgo'
    allowed_domains = ['letgo.com/en', 'search-products-pwa.letgo.com']
    start_urls = ['https://search-products-pwa.letgo.com/api/products?country_code=US&offset=0&quadkey=0320030123201&num_results=50&distance_radius=50&distance_type=mi']
    offset = 0
    
    def parse(self, response):
        data = json.loads(response.text)
        while len(data) != 0:
            for used_item in data:
                try:
                    if used_item['name'] == None:
                        title = used_item['image_information']
                    else:
                        title = used_item['name']
                    id_number = used_item['id']
                    price = used_item['price']
                    description = used_item['description']
                    date = used_item['updated_at']
                    images = [img['url'] for img in used_item['images']]
                    latitude = used_item['geo']['lat']
                    longitude = used_item['geo']['lng']
                    link = 'https://us.letgo.com/en/i/' + re.sub(r'\W+', '-', title) + '_' + id_number
                    location = used_item['geo']['city']
                except Exception:
                    pass

                yield {'Title': title,
                       'Url': link,
                       'Price': price,
                       'Description': description,
                       'Date': date,
                       'Images': images,
                       'Latitude': latitude,
                       'Longitude': longitude,
                       'Location': location,
                       }    
        
        self.offset += 50
        new_request = 'https://search-products-pwa.letgo.com/api/products?country_code=US&offset=' + str(self.offset) + \
                      '&quadkey=0320030123201&num_results=50&distance_radius=50&distance_type=mi'
        print(new_request)
        sleep(1)
        yield scrapy.Request(new_request, callback=self.parse)
            
        
