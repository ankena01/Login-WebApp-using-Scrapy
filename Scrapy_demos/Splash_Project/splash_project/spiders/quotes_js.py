import scrapy
from scrapy_splash import SplashRequest

#### Scrapy shell command -> scrapy shell "http://127.0.0.1:8060/render.html?url=https://quotes.toscrape.com/js/&wait=5"




lua_script = """function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end"""



class QuotesJsSpider(scrapy.Spider):
    name = "quotes_js"
    allowed_domains = ["quotes.toscrape.com", "127.0.0.1"]
    # start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"    
        yield SplashRequest(url, callback=self.parse, args={"lua_script" : lua_script})

    def parse(self, response):
        # Logic to parse

        quotes = response.xpath("//div[@class='quote']/span[@class='text']/text()").extract()
        
        yield {"Quotes" : quotes}

        # next_page = response.xpath("//li[@class='next']/a/@href").get()

        # yield SplashRequest(url=response.urljoin(next_page), callback= self.parse)

    
