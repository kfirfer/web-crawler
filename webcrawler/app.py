# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor

from webcrawler.loggings.logger import logger
from webcrawler.service.webcrawler import start_crawl

log = logger(__name__)


def run():
    threads = int(os.environ["THREADS"])
    executor = ThreadPoolExecutor(max_workers=threads)
    for _ in range(0, threads):
        executor.submit(run_thread)


def run_thread():
    while True:
        try:
            start_crawl()
        except Exception as e:
            log.exception(e)
            log.info("Sleep for 60 seconds")
            time.sleep(60)
        finally:
            log.info("Sleep for 600 seconds")
            time.sleep(600)
