# -*- coding: utf-8 -*-
import atexit
import os
import sys
import traceback
import warnings
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy import exc as sa_exc
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.query import Query as _Query

from webcrawler.config.mysql import db

echo = False
if 'MYSQL_LOG_QUERIES' in os.environ and os.environ["MYSQL_LOG_QUERIES"] == "1":
    echo = True

uri = "mysql://{}:{}@{}:{}/{}?use_unicode=1&charset=utf8mb4".format(os.environ["MYSQL_USER"],
                                                                    os.environ["MYSQL_PASSWORD"],
                                                                    os.environ["MYSQL_HOST"],
                                                                    os.environ["MYSQL_PORT"],
                                                                    os.environ["MYSQL_SCHEME"])

MAX_RETRY_COUNT = 0
if "MYSQL_QUERY_MAX_RETRY_COUNT" in os.environ:
    MAX_RETRY_COUNT = int(os.environ["MYSQL_QUERY_MAX_RETRY_COUNT"])


class RetryingQuery(_Query):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            try:
                return super().__iter__()
            except OperationalError:
                attempts += 1
                if attempts <= MAX_RETRY_COUNT:
                    sleep_for = 2 ** (attempts - 1)
                    sleep(sleep_for)
                    continue
                else:
                    raise


engine = create_engine(uri, pool_pre_ping=True,
                       pool_size=100, max_overflow=0, echo=echo)
session = scoped_session(sessionmaker(autocommit=True, bind=engine, query_cls=RetryingQuery))


class SqlBase(object):

    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            getattr(self, attr)
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    @staticmethod
    def _flush():
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


new_base = declarative_base(cls=SqlBase)
new_base.query = session.query_property()
new_base.query_function = session.query
new_base.execute = session.execute
automap_base = automap_base(declarative_base=new_base)


def classname_for_table(base, tablename, table):
    schema_name = table.schema
    fqname = '{}.{}'.format(schema_name, tablename)
    return fqname


def _name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    return referred_cls.__name__.split(".")[1].lower() + "_scalar"


def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    return referred_cls.__name__.split(".")[1].lower() + "_collection"


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=sa_exc.SAWarning)
    automap_base.prepare(engine=engine, reflect=True, classname_for_table=classname_for_table,
                         schema=os.environ["MYSQL_SCHEME"],
                         name_for_collection_relationship=_name_for_collection_relationship,
                         name_for_scalar_relationship=_name_for_scalar_relationship)

db.register_classes(automap_base, db.__dict__)


def exit_handler():
    try:
        session.remove()
        engine.dispose()
    except(KeyboardInterrupt, SystemExit):
        print(traceback.format_exc(), file=sys.stderr)


atexit.register(exit_handler)
