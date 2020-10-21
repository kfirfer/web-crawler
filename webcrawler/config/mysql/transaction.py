# -*- coding: utf-8 -*-
from webcrawler.config.mysql.connection import session


def transaction(func):
    def inner(*args, **kwargs):
        try:
            session.begin()
            value = func(*args, **kwargs)
            session.expunge_all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.remove()
        return value

    return inner
