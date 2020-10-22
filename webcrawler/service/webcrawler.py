# -*- coding: utf-8 -*-
import json
import os
import threading
from urllib.parse import urlparse

import pika

from webcrawler.loggings.logger import logger
from webcrawler.repository.sites import update_ratio, get_next_sites
from webcrawler.service.rabbitmq import push_to_queue
from webcrawler.util.webreader import links_from_url

log = logger(__name__)

CREDENTIALS = pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"])
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
HEADERS = {
    "Accept": "text/html"
}


def start_crawl():
    for _ in range(0, 10):
        thread = threading.Thread(target=listening_to_queue)
        thread.setDaemon(True)
        thread.start()

    sites = get_next_sites()
    for site in sites:
        url = site.url
        domain = urlparse(url).netloc
        doc = {
            "id": site.id,
            "domain": domain,
            "url": url,
            "depth": site.depth,
            "counter_same_domain": -1,
            "counter_number_of_urls": 0
        }
        push_to_queue(doc)


def listening_to_queue():
    while True:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=CREDENTIALS))
        channel = connection.channel()
        channel.basic_consume(consumer_callback=parse, queue='ml')
        channel.start_consuming()


def finished_crawl_the_end_node(doc):
    update_ratio(doc["id"], doc["counter_same_domain"], doc["counter_number_of_urls"])


def parse(ch, method, properties, body):
    log.info("Item consumed")
    doc = json.loads(body)
    url = doc["url"]
    doc["depth"] = doc["depth"] - 1
    domain = doc["domain"]
    doc["counter_number_of_urls"] = doc["counter_number_of_urls"] + 1

    current_domain = urlparse(url).netloc
    if domain == current_domain:
        doc["counter_same_domain"] += 1
    if doc["depth"] < 0:
        finished_crawl_the_end_node(doc)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    links = links_from_url(url, cache=True, headers=HEADERS)
    if len(links) == 0:
        finished_crawl_the_end_node(doc)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    for link in links:
        doc["url"] = link
        push_to_queue(doc)
    ch.basic_ack(delivery_tag=method.delivery_tag)
