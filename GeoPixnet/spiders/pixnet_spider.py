import scrapy
import re
from TaiwanAddressParser.parser import parseArticle
from GeoPixnet.items import GeopixnetItem


class PixnetSpider(scrapy.Spider):

    name = "pixnet"
    allowed_domains = ['pixnet.net']
    custom_settings = {
            #'DEPTH_LIMIT'   :10,
            'DOWNLOAD_DELAY':0.75
        }
    start_urls = [
            "https://www.pixnet.net/blog/articles/category/26",
            "https://www.pixnet.net/blog/articles/category/26/hot/2",
            "https://www.pixnet.net/blog/articles/category/26/hot/3",
            "https://www.pixnet.net/blog/articles/category/26/hot/4",
            "https://www.pixnet.net/blog/articles/category/26/hot/5",
            "https://www.pixnet.net/blog/articles/category/26/hot/6",
            "https://www.pixnet.net/blog/articles/category/26/hot/7",
            "https://www.pixnet.net/blog/articles/category/26/hot/8",
            "https://www.pixnet.net/blog/articles/category/26/hot/9",
            "https://www.pixnet.net/blog/articles/category/26/hot/10",
            ]

    

    def parse(self, response):
        

        #check the url is article url
        if re.match("http:\/\/.*\.pixnet\.net\/blog\/post\/", response.url):
            if response.css('a.topbar__related-article__cat-name::text').extract_first() == "美味食記":
                url = response.css('head>meta[property="og:url"]::attr(content)').extract_first()  
                title = response.css('head>meta[property="og:title"]::attr(content)').extract_first() 
                desc = response.css('head>meta[property="og:description"]::attr(content)').extract_first()       
                images = response.css('head>meta[property="og:image"]::attr(content)').extract()
                addresses = parseArticle(response.css('#article-content-inner').extract_first())
                if addresses: 
                    for address in addresses:
                        item = GeopixnetItem() 
                        item['url'] = url
                        item['title'] = title
                        item['desc'] = desc
                        item['images'] = images
                        item['address'] = address[0]
                        #GeoJson lng,lat
                        item['location'] = {"type":"Point", "coordinates":[address[2],address[1]]}
                        yield item
                        #items.append(item)
                        print (item, flush=True)
            #avoid goint into other categories
            else: return
            

        for url in response.css('a[href*=http]::attr(href)').extract():
            if re.match("http:\/\/.*\.pixnet\.net\/blog\/post\/", url):
                yield scrapy.Request(url, callback=self.parse)
        
