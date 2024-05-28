import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

url = "https://www.electronet.gr/pliroforiki/laptops"    

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)
time.sleep(20)