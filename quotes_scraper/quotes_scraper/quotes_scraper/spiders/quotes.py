# Import de scrapy framework
import scrapy


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

    # Define obligatory method into Spider Class
    # This method analizes a file to extract information
    # and extrat information we need
    def parse(self, response):
        print('*'*20)
        print('\n')
        print(response.status, response.headers)
        print('*'*20)
        print('\n\n')

