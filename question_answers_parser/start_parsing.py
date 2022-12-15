
import logging
import redis
import subprocess
from multiprocessing import Process
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

rd = redis.Redis(host='localhost',
                 port=6379)

subprocess.call(["scrapy", "crawl", "letter_links_crawler"])

processes = 100

def again():
    b = threading.Thread(target=worker)
    b.start()
    b.join()


def worker():
    logging.debug(
        '____________________________ TAKING NEW LINK ____________________________')
    
    subprocess.call(["scrapy", "crawl", "parse_questions_answers"])

    if rd.llen('letter_links') > 0:
        again()


for i in range(processes):
    globals()[f"my_variable_{i}"] = threading.Thread(target=worker)
    
for i in range(processes):
    globals()[f"my_variable_{i}"].start()

for i in range(processes):
    globals()[f"my_variable_{i}"].join()
