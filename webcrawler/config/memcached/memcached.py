# -*- coding: utf-8 -*-
import os

from cachelib import MemcachedCache

from webcrawler.loggings.logger import logger
from webcrawler.util.util import Singleton

log = logger(__name__)


class Memcached(metaclass=Singleton):
    r"""
    Memcached

    Environments variables:


    * MEMCACHED_HOSTS
        Memcached's hosts

        can be multiple hosts separated by ","

        for example: "10.0.0.1:11211,10,0.0.2:11212"

    Examples usage:

    os.environ['MEMCACHED_HOSTS'] = "127.0.0.1:11211"

    memcached = Memcached()

    value = memcached("some_key")
    """
    client = None
    hosts = None

    def __init__(self):
        if 'MEMCACHED_HOSTS' in os.environ:
            memcahed_hosts = os.environ['MEMCACHED_HOSTS']
            client_hosts = []
            memcahed_hosts = dict(item.split(":") for item in memcahed_hosts.split(","))

            for key, value in memcahed_hosts.items():
                client_hosts.append((key, int(value)))
            self.hosts = client_hosts
            self.client = MemcachedCache(self.hosts)

    def get_set(self, key, value, expire=3600):
        if not key or not value:
            return None
        prev_value = self.get(key)
        self.set(key, value, expire=expire)
        return prev_value

    def get(self, key):
        if not key or len(key) > 250:
            return None
        return self.client.get(key)

    def set(self, key, value, expire=3600):
        if len(key) > 250:
            return False
        self.client.set(key, value, timeout=expire)
        return True
