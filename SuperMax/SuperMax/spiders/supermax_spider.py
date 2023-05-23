"""
In scrapy shell:
    1) headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36'}
    2) fetch('https://www.supermaxonline.com/shopping-home.html', headers=headers)
    3) products = response.css('div.product-space') 
    4) name = products.css('h3 a::text').get()
    5) price = products.css('p.text-center.precio::text').get().replace('$', '').strip()
    6) link = products.css('h3 a::attr(href)').get()
"""

import scrapy

class SupMaxSpider(scrapy.Spider):
    name = 'SupMaxSpider'
    start_urls = ['https://www.supermaxonline.com/shopping-home.html']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36'}


    def parse(self, response):
        status_code = response.status
        print(f"Status code: {status_code}")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)
        