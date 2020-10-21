import os
import time
from concurrent.futures import ThreadPoolExecutor

from webcrawler.loggings.logger import logger
from webcrawler.util.mailer import Mailer

log = logger('webcrawler')
mailer = Mailer()


def run():
    threads = int(os.environ["THREADS"])
    executor = ThreadPoolExecutor(max_workers=threads)
    for i in range(0, threads):
        executor.submit(run_thread)


def run_thread():
    while True:
        try:
            log.info("bla")
        except Exception as e:
            log.exception(e)
            log.info("Sleep for 60 seconds")
            time.sleep(60)
        finally:
            log.info("Sleep for 30 seconds")
            time.sleep(30)