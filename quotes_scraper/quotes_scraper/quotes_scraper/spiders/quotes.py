# Import de scrapy framework
import scrapy

# XPATH EXPRESSIONS
# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tag = //div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()

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

        title = response.xpath('//h1/a/text()').get()
        print(f'Titulo: {title}')
        print('\n')

        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        print(f'Citas: ')
        for quote in quotes:
            print(f'- {quote} ')
        print('\n')

        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()').getall()
        i = 0
        for tag in top_ten_tags:
            i += 1
            print(f'{i}.- {tag}')
        print('\n')
        
        #print(response.status, response.headers)
        print('*'*20)
        print('\n\n')

