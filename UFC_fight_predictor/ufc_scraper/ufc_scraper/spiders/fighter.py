import scrapy


class FighterSpider(scrapy.Spider):
    name = "fighter"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/fighters"]

    def parse(self, response):
        pass
