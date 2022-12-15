from ..items import HeaderItem
import scrapy
import redis
from scrapy.spiders import CrawlSpider
from scrapy import Request
import mysql.connector


rd = redis.Redis(host='localhost',
                 port=6379)

mydb = mysql.connector.connect(
                    host="localhost",
                    user="hampni",
                    password="2481632",
                    database='pythonParser'
                )
mycursor = mydb.cursor()


class ParseQuestionsAnswersSpider(CrawlSpider):
    name = 'parse_questions_answers'
    allowed_domains = ['kreuzwort-raetsel.net']

    def start_requests(self):
        request = Request((rd.lpop('letter_links')).decode('utf-8'),callback=self.parse)
        yield request
    
    def parse(self, response):
        for tbody in response.css('tbody'):
            for tr in tbody.css('tr'):

                item = HeaderItem()

                for td in tr.css('.AnswerShort'):
                    for a in td.css('a'):
                        answer = a.css('::text').extract()
                        item['answer'] = answer
                        
                for td in tr.css('.Question'):
                    for a in td.css('a'):
                        question = a.css('::text').extract()
                        item['question'] = question

                # Check if such question exists in the db
                mycursor.execute(
                    "SELECT id FROM Questions WHERE question = %s", ([item['question'][0]]))
                questionCheck = mycursor.fetchone()
    
                # mycursor.reset()
    
                # Check if such answer exists in the db
                mycursor.execute(
                    "SELECT id FROM Answers WHERE answer = %s", ([item['answer'][0]]))
                answerCheck = mycursor.fetchone()
    
                # mycursor.reset()           
    
                if questionCheck == None:
                    mycursor.execute(
                        "INSERT INTO Questions (question) VALUES (%s)", ([item['question'][0]]))
                    mydb.commit()
                    
                # mycursor.reset()
    
                if answerCheck == None:
                    mycursor.execute(
                        "INSERT INTO Answers (answer, length) VALUES (%s, %s)", ([item['answer'][0], len(item['answer'][0])]))
                    mydb.commit()
    
                # mycursor.reset()
                    
                # question
                mycursor.execute(
                "SELECT id FROM Questions WHERE question = %s", ([item['question'][0]]))
                insertedQuestion = mycursor.fetchone()
                
                # mycursor.reset()
    
                # answer
                mycursor.execute(
                "SELECT id FROM Answers WHERE answer = %s", ([item['answer'][0]]))
                insertedAnswer = mycursor.fetchone()
                
                # mycursor.reset()
    
                mycursor.execute(
                    "SELECT * FROM question_answer WHERE question_id = %s AND answer_id = %s", ([insertedQuestion[0], insertedAnswer[0]]))
                check = mycursor.fetchone()
    
                # mycursor.reset()
                
                if check == None:
                    mycursor.execute(
                        "INSERT INTO question_answer (question_id, answer_id) VALUES (%s, %s)", ([insertedQuestion[0], insertedAnswer[0]]))
        mydb.commit()
                    
        mycursor.close()
    
        mydb.close() 
    
        print('_____________________________ FINISHED WITH____________________________' + response.url)
    