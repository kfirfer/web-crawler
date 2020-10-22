# -*- coding: utf-8 -*-
import os

os.environ["THREADS"] = os.getenv("THREADS", "1")
os.environ["LOGGER_LEVEL"] = os.getenv("LOGGER_LEVEL", "debug")
os.environ["LOG_CURL_REQUESTS"] = os.getenv("LOG_CURL_REQUESTS", "1")
os.environ["MYSQL_LOG_QUERIES"] = os.getenv("MYSQL_LOG_QUERIES", "0")

os.environ["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
os.environ["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "123123")
os.environ["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "127.0.0.1")
os.environ["MYSQL_PORT"] = os.getenv("MYSQL_PORT", "3309")
os.environ["MYSQL_SCHEME"] = os.getenv("MYSQL_SCHEME", "webcrawler")
os.environ["JSON_LOG_CONSOLE"] = os.getenv("JSON_LOG_CONSOLE", "0")
os.environ["MEMCACHED_HOSTS"] = os.getenv("MEMCACHED_HOSTS", "127.0.0.1:11211")

os.environ["RABBITMQ_USER"] = os.getenv("RABBITMQ_USER", "admin")
os.environ["RABBITMQ_HOST"] = os.getenv("RABBITMQ_HOST", "127.0.0.1")
os.environ["RABBITMQ_PASSWORD"] = os.getenv("RABBITMQ_PASSWORD", "admin")
os.environ["RABBITMQ_EXCHANGE"] = os.getenv("RABBITMQ_EXCHANGE", "exchange")

os.environ["DEBUG_MODE"] = os.getenv("DEBUG_MODE", "1")
