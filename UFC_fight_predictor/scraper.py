import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase
import pandas as pd
import re
import scrapy




def get_urls(target_url='http://ufcstats.com/statistics/fighters?char='):
    urls = []
    for char in ascii_lowercase:
        final_url = url + char + end_url
        urls.append(final_url)
    return urls


class FighterScraper:

    def fetch(self, url):
        print('HTTP GET request to URL: {}'.format(url))

        res = requests.get(url)

class UFCScraper(scrapy.Spider):
    name = "ufc_scraper"
    allowed_domains = ["pubmed.ncbi.nlm.nih.gov"]
    start_urls = []

    beginning_url = 'https://pubmed.ncbi.nlm.nih.gov/?term='
    search_term = input('What would you like to search? \n')
    end_url = '&filter=simsearch1.fha&size=200&page='
    end_num = 5
    #end_num = 180

    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })

    for i in range(1, end_num):
        url = beginning_url + search_term + end_url + str(i)
        start_urls.append(url)

    # might need a start_request function
    '''
    def start_request(self):
        yield scrapy.Request('web_address')
    '''

    def parse(self, response):

        # get all the paper links on the search page
        for link in response.css('article.full-docsum a::attr(href)'):
            # loop through the links and call parse_paper on each link
            yield response.follow(link.get(), callback=self.parse_paper)

    def parse_paper(self, response):
        try:
            yield {
                'paper_title': response.css('h1.heading-title::text').get().strip(),
                'authors': response.css('span.authors-list-item a::text').getall(),
                'date': response.css('span.secondary-date::text').get().strip(),
                'abstract': response.css('div#eng-abstract p::text').get().strip()
            }
        except:
            yield {
                'paper_title': response.css('h1.heading-title::text').get().strip(),
                'authors': response.css('span.authors-list-item a::text').getall(),
                'date': 'None',
                'abstract': response.css('div#eng-abstract p::text').get().strip()
            }






# scrape fight data

# Mutate data to show fighters and their stat differential
'''
event = response.xpath('/html/body/section/div/div/div/div[2]/div/table/tbody/tr[2]/td[1]/i/a/@href').extract()


# fight table to loop through
fight_table = '/html/body/section/div/div/table'

fight = response.xpath('/html/body/section/div/div/table/tbody/tr[1]/td[1]/p/a/@href').extract()

fighter_a = response.xpath('/html/body/section/div/div/div[1]/div[1]/div/h3/a/text()').extract_first().strip()
fighter_b = response.xpath('/html/body/section/div/div/div[1]/div[2]/div/h3/a/text()').extract_first().strip()

# First fighter is always the winner for past events in the case of a D/NC it will be marked as such
winner = response.xpath('/html/body/section/div/div/div[1]/div[1]/i/text()').extract_first().strip()
method = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]/text ()').extract().strip()
'''