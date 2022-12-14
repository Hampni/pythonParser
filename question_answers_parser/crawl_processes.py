# import threading
# import subprocess
# import redis

# rd = redis.Redis(host='localhost',
#                  port=6379)


# def writer():
#     subprocess.call(["scrapy", "crawl", "parse_questions_answers"])

# procs = 10

# while rd.llen('letter_links') > 0:

#     for i in range(procs):
#         globals()[f"my_variable_{i}"] = threading.Thread(target=writer)

#     for i in range(procs):
#         globals()[f"my_variable_{i}"].start()

#     for i in range(procs):
#         globals()[f"my_variable_{i}"].join()
import mysql.connector



mydb = mysql.connector.connect(
    host="localhost",
    user="hampni",
    password="2481632",
    database='pythonParser'
)

mycursor = mydb.cursor()

mycursor.execute(
    "SELECT * FROM Questions WHERE question = %s", (['GIJON']))
questionCheck = mycursor.fetchone()
print(questionCheck[0])

mycursor.close()
