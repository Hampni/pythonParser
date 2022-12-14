
import redis
import subprocess
from multiprocessing import Process
import threading

rd = redis.Redis(host='localhost',
                 port=6379)

procs = 100

circles = round(rd.llen('letter_links') / procs)

print(circles)

def writer():
    subprocess.call(["scrapy", "crawl", "parse_questions_answers"])

for i in range(circles):
    for i in range(procs):
        globals()[f"my_variable_{i}"] = threading.Thread(target=writer)

    for i in range(procs):
        globals()[f"my_variable_{i}"].start()

    for i in range(procs):
        globals()[f"my_variable_{i}"].join()