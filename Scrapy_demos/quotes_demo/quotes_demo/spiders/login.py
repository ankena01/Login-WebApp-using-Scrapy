import scrapy
from scrapy.http import FormRequest
from ..items import QuotesDemoItem

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]
    page_number = 2

    def parse(self, response):
        # Login

        token = response.xpath('//form[@action="/login"]/input[@name="csrf_token"]/@value').get()
        username = 'demo_1'
        password = 'demo_1'
        
        return FormRequest.from_response(response,formdata={'csrf_token' : token,'username':username,'password':password}, callback=self.start_scraping)
    
    def start_scraping(self,response):
        items = QuotesDemoItem()        

        # #finding the title of the web page
        # title = response.css("title::text").extract()[-1]
        # yield {'title_text' : title}


        ## get all quotes , authors , titles

        all_div_quotes = response.css("div.quote")

        
        for quotes in all_div_quotes:
            # tags = []
            quote = quotes.css("span.text::text").extract()
            author = quotes.css("small.author::text").extract()
            ### Method 1
            tag_s =quotes.css("a.tag::text").extract()         
            
            # yield {"Quotes" : quote,
            #         "Author" : author,
            #         "Tags" : tag_s}
            
            items['quotes'] = quote
            items['author'] = author
            items['tags'] = tag_s
            
            yield items


        # #Crawl through multiple pages using 'Next' Button
        # next_page = response.xpath('//li[@class="next"]/a/@href').get()
        # if next_page is not None:
        #     # Sending request to next page
        #     yield response.follow(next_page,callback=self.start_scraping)


        # ### Pagination
        # next_page = f"https://quotes.toscrape.com/page/{LoginSpider.page_number}/"

        # if LoginSpider.page_number < 11:
        #     LoginSpider.page_number +=1 
        #     yield response.follow(next_page, callback = self.start_scraping)
        
        #### navigate through each page using absolute (complete) url path

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        
        yield scrapy.Request(response.urljoin(next_page) , callback=self.start_scraping)

