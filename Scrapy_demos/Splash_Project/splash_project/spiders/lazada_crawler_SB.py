from typing import Iterable
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request, FormRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from logging import Logger
from ..items import SplashProjectItem

class LazadaCrawlerSpider(scrapy.Spider):
    name = "lazada_crawler_SB"
    allowed_domains = ["www.lazada.com.my"]
    # start_urls = ["https://www.lazada.com.my/"]

    def start_requests(self):
        url = "https://www.lazada.com.my/"
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url)
        time.sleep(10)
        sel = Selector(text=self.driver.page_source)
        all_product_urls = sel.xpath("//div[@class='rax-view-v2 card-jfy-wrapper']/a/@href").extract()

        self.body = self.driver.page_source.encode('utf-8')
        self.response = HtmlResponse(url = self.driver.current_url, body = self.body)
        ### Create


        for product_url in all_product_urls:
            final_url = self.response.urljoin(product_url)
            # print("---------------------- I am inside start request ----------------------")
            # print(final_url)
            yield Request(final_url, callback=self.parse)
            break
           


    def parse(self, response):
        items = SplashProjectItem()
        self.driver.get(response.url)
        time.sleep(3)
        sel = Selector(text=self.driver.page_source)
        self.driver.close()

        product_name = sel.xpath("//div[@class='pdp-mod-product-badge-wrapper']/h1[@class='pdp-mod-product-badge-title']/text()").extract()

        # product_price = sel.xpath("//div[@class='pdp-product-price']/span[@class='notranslate pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl']/text()").extract()

        product_price = sel.xpath("//div[@class='pdp-product-price']/child::span/text()").extract()

        # product_img_url = sel.xpath("//div[@class='gallery-preview-panel__content']/img[@class='pdp-mod-common-image gallery-preview-panel__image']/@src").extract_first()




        review_count = sel.xpath("//div[@class='pdp-review-summary']/child::a/text()").extract()

        items['productname']  = product_name
        items['productprice']  = product_price
        items['reviewcount']  = review_count
        # items['image_urls']  = response.urljoin(product_img_url)

        yield items

        # yield {
        #     "Product Name" : product_name, 
        #     "Product Price" : product_price,
        #     "Review Count" : review_count,
        #     "Image URL" : product_img_url
        # }


        
        
