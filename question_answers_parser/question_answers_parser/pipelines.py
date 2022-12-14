# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


# class QuestionAnswersParserPipeline:
#     def process_item(self, item, spider):
#         return item


class QuestionAnswersParserPipeline():
    def process_item(self, item, spider):
        if spider.name in ['parse_questions_answers']:
            
            mydb = mysql.connector.connect(
                host="localhost",
                user="hampni",
                password="2481632",
                database='pythonParser'
            )
            
            mycursor = mydb.cursor()

            # Check if such question exists in the db
            mycursor.execute(
                "SELECT * FROM Questions WHERE question = %s", ([item['question']]))
            questionCheck = mycursor.fetchone()

            mycursor.reset()

            # Check if such answer exists in the db
            mycursor.execute(
                "SELECT * FROM Answers WHERE answer = %s", ([item['answer']]))
            answerCheck = mycursor.fetchone()

            mycursor.reset()           

            if questionCheck == None:
                mycursor.execute(
                    "INSERT INTO Questions (question) VALUES (%s)", ([item['question']]))
                mydb.commit()
                
            mycursor.reset()

            if answerCheck == None:
                mycursor.execute(
                    "INSERT INTO Answers (answer, length) VALUES (%s, %s)", ([item['answer'], len(item['answer'])]))
                mydb.commit()

            mycursor.reset()
                
            # question
            mycursor.execute(
            "SELECT * FROM Questions WHERE question = %s", ([item['question']]))
            insertedQuestion = mycursor.fetchone()
            
            mycursor.reset()

            # answer
            mycursor.execute(
            "SELECT * FROM Answers WHERE answer = %s", ([item['answer']]))
            insertedAnswer = mycursor.fetchone()
            
            mycursor.reset()

            mycursor.execute(
                "SELECT * FROM question_answer WHERE question_id = %s AND answer_id = %s", ([insertedQuestion[0], insertedAnswer[0]]))
            check = mycursor.fetchone()

            mycursor.reset()
            
            if check == None:
                mycursor.execute(
                    "INSERT INTO question_answer (question_id, answer_id) VALUES (%s, %s)", ([insertedQuestion[0], insertedAnswer[0]]))
                mydb.commit()
                
            mycursor.close()

            mydb.close() 

