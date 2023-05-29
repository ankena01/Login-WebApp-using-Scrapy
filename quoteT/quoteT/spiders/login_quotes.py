import scrapy

from scrapy.http import Request , FormRequest


class LoginQuotesSpider(scrapy.Spider):
    name = "login_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]
    page_number = 2

    def parse(self, response):
        # implement the login functionality

        token = response.css("form input::attr(value)").extract_first()
        username = "ankur"
        password = "ankur"

        return FormRequest.from_response(response, formdata={'csrf_token' : token, 'username' : username, 'password': password}, callback = self.start_scraping)

    def start_scraping(self, response):
        
        
        
        # Logic to scrape 
        

        # Get title on the web page
        title = response.css("title::text").extract()

        # Web scraping of quotes, authors, tags

        all_div_quotes = response.css(".quote")

        for quotes in all_div_quotes:
            quote = quotes.css(".text::text").extract_first()
            author = quotes.css(".author::text").extract_first()
            tag = quotes.css(".tags .tag").css("::text").extract()

            yield {'Title' : title, 'quote' : quote , 'Author': author , 'Tag' : tag}
        

        next_page = f"https://quotes.toscrape.com/page/{LoginQuotesSpider.page_number}/"

        if LoginQuotesSpider.page_number < 11:
            # next_page += 1

            LoginQuotesSpider.page_number = LoginQuotesSpider.page_number + 1

            # go to next page
            yield response.follow(next_page, callback = self.start_scraping)


