import scrapy
import redis
from scrapy.spiders import CrawlSpider

rd = redis.Redis(host='localhost',
                 port=6379)


class CrawlingSpider(CrawlSpider):
    name = "letter_links_crawler"
    allowed_domains = ["kreuzwort-raetsel.net"]
    start_urls = ["https://kreuzwort-raetsel.net/"]
    pipelines = ['pipeline1']

    def start_requests(self):
        urls = [
            'https://kreuzwort-raetsel.net/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_homepage)

    def parse_homepage(self, response):   
        for ul in response.css('.dnrg'):
            for li in ul.css("li"):
                url = 'https://kreuzwort-raetsel.net/' + li.css("a::attr('href')").get()
                yield scrapy.Request(url=url, callback = self.parse_letters)

    def parse_letters(self, response):
        for ul in response.css('.dnrg'):
            for li in ul.css('li'):
                rd.rpush('letter_links', 'https://kreuzwort-raetsel.net/' + li.css("::attr('href')").get())
               

            
