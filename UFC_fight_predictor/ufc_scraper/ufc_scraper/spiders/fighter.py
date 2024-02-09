import scrapy
from string import ascii_lowercase
from ufc_scraper.items import UfcScraperItem


class FighterSpider(scrapy.Spider):
    name = "fighter"    

    def start_requests(self):
        start_url = "http://ufcstats.com/statistics/fighters?char="
        end_url = "&page=all"
        urls = [start_url + char + end_url for char in ascii_lowercase]
        urls = urls[:1]

        # for each url add in a second loop to get all the fighters hrefs
            
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_fighter_page)
    
    def parse_fighter_page(self, response):
        # Extract hrefs for each fighter on the current page
        rows = response.xpath('/html/body/section/div/div/div/table/tbody/tr')
        
        for row in rows:
            href = row.xpath('td[1]/a/@href').extract_first()
            if href:
                yield response.follow(str(href), callback=self.parse_fighter_details)
        
        
    def parse_fighter_details(self, response):
        fight = UfcScraperItem()
        fight['fighter_id'] = response.url.split('/')[-1]
        fight['name'] = response.xpath('/html/body/section/div/h2/span[1]/text()').extract_first().strip()
        fight['height'] = response.xpath('/html/body/section/div/div/div[1]/ul/li[1]/text()').extract()[1].strip()
        fight['weight'] = response.xpath('/html/body/section/div/div/div[1]/ul/li[2]/text()').extract()[1].strip()
        fight['reach'] = response.xpath('/html/body/section/div/div/div[1]/ul/li[3]/text()').extract()[1].strip()
        fight['stance'] = response.xpath('/html/body/section/div/div/div[1]/ul/li[4]/text()').extract()[1].strip()
        fight['dob'] = response.xpath('/html/body/section/div/div/div[1]/ul/li[5]/text()').extract()[1].strip()
        fight['SLpM'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[1]/text()').extract()[1].strip()
        fight['str_acc'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[2]/text()').extract()[1].strip()
        fight['SApM'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[3]/text()').extract()[1].strip()
        fight['str_def'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[4]/text()').extract()[1].strip()
        fight['TD_avg'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[2]/text()').extract()[1].strip()
        fight['TD_acc'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[3]/text()').extract()[1].strip()
        fight['TD_def'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[4]/text()').extract()[1].strip()
        fight['sub_avg'] = response.xpath('/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[5]/text()').extract()[1].strip()
        yield fight
      
