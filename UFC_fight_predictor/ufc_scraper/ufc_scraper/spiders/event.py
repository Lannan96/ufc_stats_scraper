import scrapy
from ufc_scraper.items import ufc_event_item


class EventSpider(scrapy.Spider):
    name = "event"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
    
    def start_requests(self):
        start_urls = "http://ufcstats.com/statistics/events/completed?page=all"
            
        yield scrapy.Request(str(start_urls), callback=self.parse_event_details)

    def parse_event_details(self, response):
        event = ufc_event_item()
        event_id = response.xpath('/html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/a/@href').extract()
        event_name = response.xpath('/html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/a/text()').extract()
        date = response.xpath('/html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/span/text()').extract()
        location = response.xpath('/html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[2]/text()').extract()
        yield event