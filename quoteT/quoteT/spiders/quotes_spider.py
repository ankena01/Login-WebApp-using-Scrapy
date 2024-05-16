import scrapy

class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    page_number = 2             # class variable (initialise to page number 2)

    def parse(self, response):
        
        # Get title on the web page
        title = response.css("title::text").extract()
        # yield {'Title Text' : title}


        # Web scraping of quotes, authors, tags

        all_div_quotes = response.css(".quote")


        for quotes in all_div_quotes:
            quote = quotes.css(".text::text").extract_first()
            author = quotes.css(".author::text").extract_first()
            tag = quotes.css(".tags .tag").css("::text").extract()

            yield {'Title' : title, 'quote' : quote , 'Author': author , 'Tag' : tag}

        # Scenario 1 - Crawl through multiple pages via 'Next Button'
        # next_page = response.css("li.next a::attr(href)").extract_first()
        # print(next_page)

        # if next_page is not None:          
        #     yield response.follow(next_page, callback = self.parse)

        # Scenario 2 - Crawl through multiple pages via Pagination

        next_page = f"https://quotes.toscrape.com/page/{QuotesSpiderSpider.page_number}/"

        if QuotesSpiderSpider.page_number < 11:
            # next_page += 1

            QuotesSpiderSpider.page_number = QuotesSpiderSpider.page_number + 1

            # go to next page
            yield response.follow(next_page, callback = self.parse)