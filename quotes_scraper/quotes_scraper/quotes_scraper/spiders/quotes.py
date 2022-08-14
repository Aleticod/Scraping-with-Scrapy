# Import de scrapy framework
from ast import parse
from gc import callbacks
import scrapy

# XPATH EXPRESSIONS
# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tag = //div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()
# Boton next = //ul[@class="pager"]//li[@class="next"]/a/@href

# Spider Class definition

class QuotesSpider(scrapy.Spider):

    # Atribures
    # Unique name that scrapy refering into project
    # This name dont should repeat in other spider class

    name = 'quotes'
    # Urls when need to request
    start_urls = [
        'http://quotes.toscrape.com/page/1'
    ]

    # Settings output

    # custom_settings = {
    #     'FEED_URI': 'quotes.json',
    #     'FEED_FORMAT': 'json'
    # }

    custom_settings = {
        'FEEDS': {
            'quotes.json' : {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True
                }

            }
        }
    }

    # Define obligatory method into Spider Class
    # This method analizes a file to extract information
    # and extrat information we need
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()
 
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()

        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }

        nex_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if nex_page_button_link:
            yield response.follow(nex_page_button_link, callback = self.parse)