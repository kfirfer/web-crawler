# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import asc, true

from webcrawler.config.mysql import db
from webcrawler.config.mysql.transaction import transaction


@transaction
def get_next_profile():
    sql = db.webcrawler.sites.query.order_by(
        asc(db.webcrawler.sites.lastCrawl))
    sql = sql.filter(db.webcrawler.sites.active == true())
    sites = sql.with_for_update().first()
    sites.update(lastCrawl=datetime.datetime.now())
    return sites
