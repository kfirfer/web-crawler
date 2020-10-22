import os
import threading
import time
from multiprocessing import Queue

import pika
from pika.exceptions import ChannelClosed, ConnectionClosed

from webcrawler.loggings.logger import logger
from webcrawler.util.util import marshal_to_json

log = logger(__name__)
CREDENTIALS = pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"])
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
queue = Queue(5000)


def init():
    for _ in range(0, 5):
        thread = threading.Thread(target=publishing)
        thread.setDaemon(True)
        thread.start()


def publishing():
    while True:
        try:
            exception_count = 0
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=CREDENTIALS))
            channel = connection.channel()
            channel.confirm_delivery()

            while True:
                exchange_name, routing_key, json_utf8 = queue.get()
                try:
                    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json_utf8,
                                          properties=pika.BasicProperties(
                                              delivery_mode=2,  # make message persistent
                                          ))
                    exception_count = 0
                except (ChannelClosed, ConnectionClosed) as e:
                    log.error("RabbitMQ channel/connection (%s) closed exception" % e, exc_info=True)
                    time.sleep(5)  # Avoid spamming
                    try:
                        connection = pika.BlockingConnection(
                            pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                      credentials=CREDENTIALS))
                        channel = connection.channel()
                        channel.confirm_delivery()
                        queue.put_nowait((exchange_name, routing_key, json_utf8))
                    except Exception:
                        log.error("Exception connecting to rabbitmq", exc_info=True)
                        time.sleep(5)
                except Exception:
                    exception_count += 1
                    if exception_count == 1:
                        log.error("Exception on RabbitMQ Crawler", exc_info=True)
                    elif exception_count % 1000 == 0:
                        log.error("{0} exceptions on RabbitMQ Crawler".format(exception_count), exc_info=True)
                    time.sleep(5)
        except Exception:
            log.error("Exception connecting to rabbitmq", exc_info=True)
            time.sleep(5)


def post(exchange_name, routing_key, json_utf8):
    try:
        queue.put((exchange_name, routing_key, json_utf8), timeout=5)
    except Exception:
        log.error("Timeout trying to post to rabbitmq. blocking...")
        queue.put((exchange_name, routing_key, json_utf8))


def push_to_queue(doc):
    try:
        json_doc_string = marshal_to_json(doc)
        log.debug("New item is going to the queue")
        post(os.environ["RABBITMQ_EXCHANGE"], "ml", json_doc_string)
        return True
    except Exception:
        log.error()
        return False


init()
