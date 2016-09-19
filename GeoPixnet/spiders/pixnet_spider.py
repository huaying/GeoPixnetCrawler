import scrapy
import re
from TaiwanAddressParser.parser import parseArticle

# 1. rule: depth:3 delay:2s
# 2. allow_domain pixnet.net
# 3. if not /blog/post: only crawl ,else grab [addr],[title],[url],[image_url] and store to mongo

class PixnetSpider(scrapy.Spider):

    name = "pixnet"
    allowed_domains = ['pixnet.net']
    custom_settings = {
            'DEPTH_LIMIT'   :2,
            'DOWNLOAD_DELAY':3
        }
    start_urls = ["https://www.pixnet.net/blog/articles/category/26"]

    def parse(self, response):
        
        #check the url is article url
        if re.match("http:\/\/.*\.pixnet\.net\/blog\/post\/", response.url):
            #item = GeopixnetItem() 
            print(response.url)
            address = parseArticle(response.css('#article-content-inner').extract_first())
            if address: print(address)

        for url in response.css('a[href*=http]::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse)
        
        return None
