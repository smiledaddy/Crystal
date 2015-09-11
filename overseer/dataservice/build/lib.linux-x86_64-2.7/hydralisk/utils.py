# -*- coding: utf-8 -*-
import logging
from sqlalchemy.exc import OperationalError

_LOGGER = logging.getLogger('hydralisk')


def retry_for_mysql_idle(func):
    def wrapper(*args, **kwargs):
        k = 3
        while k > 0:
            try:
                return func(*args, **kwargs)
            except OperationalError as e:
                _LOGGER.error("retry for mysql lost connection:%s", e)
            k -= 1
    return wrapper
