# -*- coding: utf-8 -*-


from webcrawler.config.memcached.memcached import Memcached
from webcrawler.loggings.logger import logger
from webcrawler.repository.crawler import get_next_profile


log = logger(__name__)
memcached = Memcached()


def start_crawl():
    sites = get_next_profile()
    memcached.set("sites", sites.lastCrawl)
    si = memcached.get("sites")
    log.info("bla")
