# -*- coding: utf-8 -*-
import logging
import os
import sys

import webcrawler
from webcrawler.loggings.custom_json_format_log import CustomJSONLog
from webcrawler.loggings.util import random_string


def logger(log_name=random_string(10)):
    webcrawler.loggings.init_non_web(custom_formatter=CustomJSONLog)
    log = logging.getLogger(log_name)

    level = logging.DEBUG
    if 'LOGGER_LEVEL' in os.environ:
        logger_level = os.environ['LOGGER_LEVEL'].lower()
        if logger_level == "debug":
            level = logging.DEBUG
        elif logger_level == "info":
            level = logging.INFO
        elif logger_level == "warning" or logger_level == "warn":
            level = logging.WARN
        elif logger_level == "error":
            level = logging.ERROR
    log.setLevel(level)

    log.addHandler(logging.StreamHandler(sys.stdout))
    return log
