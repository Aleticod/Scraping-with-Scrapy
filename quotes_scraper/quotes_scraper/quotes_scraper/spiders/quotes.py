# Import de scrapy framework
from ast import parse
from gc import callbacks
from xml.dom.domreg import well_known_implementations
import scrapy

# XPATH EXPRESSIONS
# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tag = //div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()
# Boton next = //ul[@class="pager"]//li[@class="next"]/a/@href
# Author = //div[@class="quote"]//small[@class="author" and @itemprop="author"]/text()


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
    #     'FEED_FORMAT': 'json',
    #     'CONCURRENT_REQUESTS': 24,
    #     'MENUSAGE_LIMIT_MB': 2048,
    #     'MENUSAGE_NOTIFY_MAIN': ['193837@gmail.com', 'harvey@gmail.com'],
    #     'ROBOTSTXT_OBEY': True,
    #     'USER_AGENT': 'PepitoMartinez',
    #     'FEED_EXPORT_ENCODING': 'utf-8',
        
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

    # Methods parse that only quotes extract
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']

        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        authors.extend(response.xpath('//div[@class="quote"]//small[@class="author" and @itemprop="author"]/text()').getall())
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors })
        else:
            if len(quotes) == len(authors):
                quotes_authors = []
                i = 0
                for quote in quotes:
                    quote_author = [quote]
                    quote_author.append(authors[i])
                    quotes_authors.append(quote_author)
                    i += 1
                
                yield {
                    'quotes_authos': quotes_authors
                }

            else:

                yield {
                    'quotes': quotes,
                    'authors': authors
                }


    # Define obligatory method into Spider Class
    # This method analizes a file to extract information
    # and extrat information we need
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()
 
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()

        authors = response.xpath('//div[@class="quote"]//small[@class="author" and @itemprop="author"]/text()').getall()

        top_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()').getall()

        # Get atribute when is passed with console

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback = self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})