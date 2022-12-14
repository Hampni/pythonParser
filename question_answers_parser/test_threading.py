
import redis
import subprocess
from multiprocessing import Process
import threading

rd = redis.Redis(host='localhost',
                 port=6379)


procs = 100

circles = round(rd.llen('letter_links') / (procs * 3))

print(circles)
print(circles)
print(circles)
print(circles)


# def f(name):
#     subprocess.call(["scrapy", "crawl", "parse_questions_answers"])
    
# # while rd.llen('letter_links') > 0:
# for i in range(circles):
#     for i in range(procs):
#         if __name__ == '__main__':
#             globals()[f"my_variable_{i}"] = Process(target=f, args=('bob',))

#     for i in range(procs):
#         globals()[f"my_variable_{i}"].start()

#     for i in range(procs):
#         globals()[f"my_variable_{i}"].join()


def writer():
    subprocess.call(["scrapy", "crawl", "parse_questions_answers"])

for i in range(circles):
    for i in range(procs):
        globals()[f"my_variable_{i}"] = threading.Thread(target=writer)

    for i in range(procs):
        globals()[f"my_variable_{i}"].start()

    for i in range(procs):
        globals()[f"my_variable_{i}"].join()