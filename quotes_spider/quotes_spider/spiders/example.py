# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['sec.gov']
    start_urls = ['https://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=4/']

    def parse(self, response):
        pass
