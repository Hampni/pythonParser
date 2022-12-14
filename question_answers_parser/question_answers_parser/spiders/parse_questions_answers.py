from ..items import HeaderItem
import scrapy
import redis
from scrapy.spiders import CrawlSpider


rd = redis.Redis(host='localhost',
                 port=6379)


class ParseQuestionsAnswersSpider(CrawlSpider):
    name = 'parse_questions_answers'
    allowed_domains = ['kreuzwort-raetsel.net']
    start_urls = ['https://kreuzwort-raetsel.net/']

    def start_requests(self):
        for i in range(3):
            yield scrapy.Request(url=(rd.lpop('letter_links')).decode('utf-8'), callback=self.parse_link)

    def parse_link(self, response):

        # def start_requests(self):
        # for i in range(10):

        #     yield scrapy.Request(url=(rd.lpop('letter_links')).decode('utf-8'), callback=self.parse_letter_link)

        # def parse_letter_link(self, response):

        if response == None:
            rd.rpush('bad_links', response.url)

        if response.status != 200:
            rd.rpush('bad_links', response.url)

        for tbody in response.css('tbody'):
            for tr in tbody.css('tr'):

                header = HeaderItem()

                for td in tr.css('.AnswerShort'):
                    for a in td.css('a'):
                        answer = a.css('::text').get()
                        header['answer'] = answer
                for td in tr.css('.Question'):
                    for a in td.css('a'):
                        question = a.css('::text').get()
                        header['question'] = question
                yield header

        print('finished with _____________________________-----------------------' + response.url)
