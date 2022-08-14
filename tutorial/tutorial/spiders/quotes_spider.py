# Import Scrapy Library
import scrapy

# Class, this define the logic to bring all informatio
# we want from internet
class QuotesSpider(scrapy.Spider): # This class inherence
    # from the class spider that is on scrapy library

    # Define two atributes
    name = 'quotes'
    # This is a list of urls that we want to point
    start_urls = [
        'http://quotes.toscrape.com/'
    ]


    # Define a method called parse
    # Define a logic to extract tha infromation
    def parse(self, response):
        # Open a file
        with open ('results.html', 'w', encoding='utf-8') as f:
            f.write(response.text) # This is a reference to content, this is the html structure


