"""
In scrapy shell:
    1) headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36'}
    2) fetch('https://www.supermaxonline.com/shopping-home.html', headers=headers)
    3) products = response.css('div.product-space') 
    4) name = products.css('h3 a::text').get()
    5) price = products.css('p.text-center.precio::text').get().replace('$', '').strip()
    6) link = products.css('h3 a::attr(href)').get()

Selecting each page link: 
    links = response.css('div#departments-menu a::attr(href)')
"""

import scrapy

class SupMaxSpider(scrapy.Spider):
    name = 'SupMaxSpider'
    start_urls = ['https://www.supermaxonline.com/shopping-home.html']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.789 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        # Extract the paths from the response
        paths = response.css('div#departments-menu a::attr(href)').getall()
        visited_urls = set()

        # Initializes recursion for each path
        for path in paths: 
            url = response.urljoin(path)
            if url not in visited_urls:
                visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_products, headers=self.headers) 


    def parse_products(self, response):
        # Check 'Load_More' button
        load_more_button = response.css('button.load-more-button')

        if load_more_button:
            yield scrapy.FormRequest.from_response(
                response,
                clickdata = scrapy.FormRequest.ClickData(class_='btn', text='Ver más'),
                callback=self.parse_products, # Recursively call while there is a 'Load_More' button
                headers=self.headers
            )

        else: # Base case
            # Scrape product info
            for products in response.css('div.product-space'):
                yield {
                    "name": products.css('h3 a::text').get(),
                    "price": products.css('p.text-center.precio::text').get().replace('$', '').strip(),
                    "link": products.css('h3 a::attr(href)').get(),
                }