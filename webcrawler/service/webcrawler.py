# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

from webcrawler.config.memcached.memcached import Memcached
from webcrawler.loggings.logger import logger
from webcrawler.service.rabbitmq import push

log = logger(__name__)
memcached = Memcached()
_listOfCrawled = set()
_domains = set()
_index = []


def start_crawl():
    # crawl("https://keycloak.tatzan.com/auth/", 1)
    doc = {
        "bla": "blabla"
    }
    push(doc)


def print_domains(links):
    for link in links:
        domain = urlparse(link).netloc
        log.info(domain)


def crawl(url, depth_to_go):
    _listOfCrawled.add(url)
    text = text_from_url(url)
    log.info(url)
    links = links_from_url(url)
    print_domains(links)
    if depth_to_go > 0:
        for i in links:
            if i not in _listOfCrawled:
                crawl(i, depth_to_go - 1)


def links_from_url(url):
    headers = {
        "Content-Type": "text/plain"
    }
    resp = requests.get(url=url, timeout=30, headers=headers)
    parser = 'html.parser'
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "http" not in href:
            continue
        links.add(href)
    return links


def text_from_url(url):
    headers = {
        "Accept": "text/html"
    }
    response = requests.get(url=url, timeout=30, headers=headers)
    return response.text
