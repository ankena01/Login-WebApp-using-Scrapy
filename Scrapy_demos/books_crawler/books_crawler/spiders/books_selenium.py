from typing import Iterable
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



class BooksSeleniumSpider(scrapy.Spider):
    name = "books_selenium"
    allowed_domains = ["books.toscrape.com"]
    # start_urls = ["https://books.toscrape.com/"]

    ## generate our initial requests dynamically
    def start_requests(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get("https://books.toscrape.com/")

        yield ...

    def parse(self, response):
        pass
