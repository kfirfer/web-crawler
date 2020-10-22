import os

import curlify
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

from webcrawler.config.memcached.memcached import Memcached
from webcrawler.loggings.logger import logger

log = logger(__name__)

print_curl = False
if "LOG_CURL_REQUESTS" in os.environ and os.environ['LOG_CURL_REQUESTS'] == "1":
    print_curl = True

memcached = Memcached()


def links_from_url(url, cache=False, headers=None):
    response = None
    if cache:
        response = memcached.get(url)
    if response is None:
        response = requests.get(url=url, timeout=30, headers=headers)
        if print_curl:
            log.debug(curlify.to_curl(response.request))
        memcached.set(url, response)
    parser = 'html.parser'
    http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(response.content, parser, from_encoding=encoding)
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "http" not in href:
            continue
        links.add(href)
    return links
