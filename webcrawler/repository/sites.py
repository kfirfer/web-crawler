# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import asc, true

from webcrawler.config.mysql import db
from webcrawler.config.mysql.transaction import transaction


@transaction
def get_next_sites():
    sql = db.webcrawler.sites.query.order_by(asc(db.webcrawler.sites.lastCrawl))
    sql = sql.filter(db.webcrawler.sites.active == true())
    sites = sql.with_for_update().limit(100)
    for site in sites:
        site.update(lastCrawl=datetime.datetime.now())
    return sites


@transaction
def update_ratio(_id, counter_same_domain, counter_number_of_urls):
    sql = db.webcrawler.sites.query.filter_by(id=_id)
    sql = sql.filter(db.webcrawler.sites.active == true())
    site = sql.with_for_update().first()
    db_counter_same_domain = site.counter_same_domain
    db_counter_number_of_urls = site.counter_number_of_urls
    counter_number_of_urls += db_counter_number_of_urls
    counter_same_domain += db_counter_same_domain
    ratio = counter_same_domain / counter_number_of_urls
    site.update(ratio=ratio, counter_number_of_urls=counter_number_of_urls, counter_same_domain=counter_same_domain)
    return site
