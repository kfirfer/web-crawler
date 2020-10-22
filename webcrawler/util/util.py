# -*- coding: utf-8 -*-
import json
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def iso_format(dt):
    try:
        utc = dt + dt.utcoffset()
    except TypeError as e:
        utc = dt
    iso_string = datetime.strftime(utc, '%Y-%m-%dT%H:%M:%S.{:03}Z')
    return iso_string.format(int(round(utc.microsecond / 1000.0)))


def marshal_to_json(item):
    json_str = json.dumps(item, ensure_ascii=False)
    return json_str
