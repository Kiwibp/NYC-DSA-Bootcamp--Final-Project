# -*- coding: utf-8 -*-
import scrapy


class FacebookMarketplaceSpider(scrapy.Spider):
    name = 'facebook_marketplace'
    allowed_domains = ['http://facebook.com/marketplace/104063499628686/']
    start_urls = ['http://facebook.com/marketplace/104063499628686//']

    def parse(self, response):
        pass
