import scrapy
from ufc_scraper.items import ufc_event_item


class EventSpider(scrapy.Spider):
    name = "event"
    allowed_domains = ["ufcstats.com"]
    
    
    def start_requests(self):
        start_urls = "http://ufcstats.com/statistics/events/completed?page=all"    
        yield scrapy.Request(str(start_urls), callback=self.parse_event_details)

    def parse_event_details(self, response):
        for row in response.xpath('//table[contains(@class, "b-statistics__table-events")]//tr')[1:]:    
            event = ufc_event_item()
            event['event_id'] = row.xpath('.//td[1]/i/a/@href').extract()
            event['event_name'] = row.xpath('.//td[1]/i/a/text()').extract()
            event['date'] = row.xpath('.//td[1]/i/span/text()').extract()
            event['location'] = row.xpath('.//td[2]/text()').extract()
            yield event