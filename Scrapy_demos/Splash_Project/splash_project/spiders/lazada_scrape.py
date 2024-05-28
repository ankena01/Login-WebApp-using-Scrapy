####   Scrapping of data points like Product Name, Price, Review Count from the homepage directly

from ..items import SplashProjectItem
from typing import Iterable
import scrapy
from scrapy.http import HtmlResponse, Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class LazadaScrapeSpider(scrapy.Spider):
    name = "lazada_scrape_selenium"
    allowed_domains = ["www.lazada.com.my"]
    # start_urls = ["https://www.lazada.com.my/#?"]

    def start_requests(self):    ### Generating dyamic Requests
        url = "https://www.lazada.com.my/#?"    

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url)
        time.sleep(5)

        ## Add logic for scroll upto load more button and then click on it (Method 1)
        self.load_more_element = self.driver.find_element(By.XPATH , "//div[@class='rax-view-v2 load-more-button']")

        time.sleep(3)
        
        ### If we want to scroll to the bottom of the page then use the below command
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        ### Scroll to the next button
        self.driver.execute_script("arguments[0].scrollIntoView({ behaviour : 'smooth', block : 'end', inline: 'end'});", self.load_more_element)
        
        time.sleep(2)

        self.load_more_element.click()
        
        time.sleep(5)

        self.body = self.driver.page_source.encode('utf-8')
        ### Add logic to find next button using scrapy selector here (Method 2)
        self.response = HtmlResponse(url=self.driver.current_url, body = self.body, encoding = 'utf-8')
        self.driver.close()     
        yield Request(url=self.response.url, callback=self.parse, meta={'response' : self.response})
        

    def parse(self, response):
        # print("--- Inside Parse")
        # print(response.url)
        
        ### Scrapping logic
        # product_title = response.meta['response'].xpath("//div[@class='rax-view-v2 card-jfy-title']/text()").extract()
        # yield {"Product Name" : product_title}


        all_products = (response.meta.get('response')).xpath("//div[@class='rax-view-v2 card-jfy-wrapper']")

        for product in all_products:
            product_name = product.xpath(".//div[@class='rax-view-v2 card-jfy-title']/text()").extract()
            product_price = product.xpath(".//div[@class='rax-view-v2 hp-mod-price-first-line']/span[@class='rax-text-v2 price']/text()").extract()
            review_count = product.xpath(".//div[@class='rax-view-v2 card-jfy-ratings-comment']/text()").extract()
            image_product = product.xpath(".//a[@class='jfy-item']/img/@src").get()
            # image = response.urljoin(image)
            # image = "https:" + image
            # yield {"Product Name" : product_name,
            #         "Product Price" : product_price,  
            #     "Review Count" : review_count,
            #     "Image URL" : image}


        items = SplashProjectItem()      
        items['productname'] = product_name
        items['productprice'] = product_price
        items['reviewcount'] =  review_count
        items['image_urls'] = image_product
        items['file_urls'] = image_product
        yield items

