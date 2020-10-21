import os

import requests
import time
import curlify

from webcrawler.loggings.logger import logger

log = logger()

print_curl = False
if "LOG_CURL_REQUESTS" in os.environ and os.environ['LOG_CURL_REQUESTS'] == "1":
    print_curl = True


def request_post(url, payload, headers, timeout, s=None, params=None):
    response = None
    for i in range(0, 3):
        try:
            if s:
                response = s.request("POST", url, data=payload, headers=headers, timeout=timeout, params=params)
            else:
                response = requests.request("POST", url, data=payload, headers=headers, timeout=timeout, params=params)
            if print_curl:
                log.debug(curlify.to_curl(response.request))
            break
        except:
            if i == 2:
                raise
            time.sleep(1)

    return response


def request_get(url, headers, timeout, s=None, params=None):
    response = None
    for i in range(0, 3):
        try:
            if s:
                response = s.request("GET", url, headers=headers, timeout=timeout, params=params)
            else:
                response = requests.request("GET", url, headers=headers, timeout=timeout, params=params)
            if print_curl:
                log.debug(curlify.to_curl(response.request))
            break
        except:
            if i == 2:
                raise
            time.sleep(1)

    return response


def http_get(url, headers=None, timeout=30, proxy=None, parse_json=False, params=None):
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        s = requests.Session()
        s.proxies = proxies
        response = request_get(url, headers, timeout, s=s, params=params)
    else:
        response = request_get(url, headers, timeout, s=None, params=params)
    if response and parse_json:
        try:
            return response.json()
        except:
            log.error("Parse Response JSON error", response=response.text, url=url)
            return None
    return response


def http_post(url, payload, headers=None, timeout=30, proxy=None, parse_json=False, params=None):
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        s = requests.Session()
        s.proxies = proxies
        response = request_post(url, payload, headers, timeout, s, params=params)
    else:
        response = request_post(url, payload, headers, timeout, params=params)

    if response and parse_json:
        try:
            return response.json()
        except:
            log.error("Parse Response JSON error", response=response.text, url=url)
            return None
    return response
