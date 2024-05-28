from typing import Iterable
import scrapy


class NtschoolScrapeSpider(scrapy.Spider):
    name = "ntschool_scrape"
    allowed_domains = ["directory.ntschools.net"]
    start_urls = ["https://directory.ntschools.net/"]
    
    headers = {"Accept": "application/json",
                "Accept-Encoding" : "gzip, deflate, br, zstd",
                "Accept-Language" : "en-US,en;q=0.9,en-IN;q=0.8",
                "Referer": "https://directory.ntschools.net/",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
                "X-Requested-With": "Fetch",
                }

    # def start_requests(self):
    #     yield scrapy.Request("https://directory.ntschools.net/api/System/GetAllSchools", headers = {})


    def parse(self, response):
        yield scrapy.Request(url = "https://directory.ntschools.net/api/System/GetAllSchools", headers=self.headers, callback=self.parse_json)

    def parse_json(self, response):
        # Here we will get all the school codes "itSchoolCode"
        # print("----------------------Response Type ----------", type(response))
        # print(response.json())
        # print("----------------------Response Type ----------", type(response.json()))
        ## Fetch itschool code for all schools and send requests to each school url

        data = response.json()

        for school in data:
            # school_code = school['itSchoolCode']
            school_code = school.get('itSchoolCode')
            # print(school_code)
            yield scrapy.Request(f"https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}", headers=self.headers, callback=self.parse_school)
            # break

    def parse_school(self,response):
        ## Get the datapoints for each school SchoolName, PhysicalAddress, PostalAddress, Email
        # print("----------------------Response Type ----------", type(response))
        # print(response.json())
        # print("----------------------Response Type ----------", type(response.json()))

        SchoolName = response.json()['name']
        PhysicalAddress = response.json()['physicalAddress']['displayAddress']
        PostalAddress = response.json()['postalAddress']['displayAddress']
        Email = response.json()['mail']


        yield {"SchoolName": SchoolName,
                "PhysicalAddress": PhysicalAddress,
                "PostalAddress": PostalAddress,
                "Email": Email}