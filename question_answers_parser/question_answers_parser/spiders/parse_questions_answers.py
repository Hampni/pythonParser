from ..items import HeaderItem
import scrapy
import redis
from scrapy.spiders import CrawlSpider
from scrapy import Request


rd = redis.Redis(host='localhost',
                 port=6379)


class ParseQuestionsAnswersSpider(CrawlSpider):
    name = 'parse_questions_answers'
    allowed_domains = ['kreuzwort-raetsel.net']

    def start_requests(self):
        request = Request((rd.lpop('letter_links')).decode('utf-8'),callback=self.parse)
        yield request
    
    def parse(self, response):

        if rd.llen('letter_links') % 10 ==0:
            print('++++++++++++++++++++++++++++++++++++++')
            print(rd.llen('letter_links'))
            print('++++++++++++++++++++++++++++++++++++++')

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
