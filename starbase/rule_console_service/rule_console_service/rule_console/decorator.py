# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps

from armory.marine.json_rsp import json_response_error
from armory.marine.respcode import PARAM_ERROR
from rule_console.api import request
from rule_console.settings import MONGO_CONFIG
from rule_console.view.common_support import get_model_cls


_LOGGER = logging.getLogger(__name__)


def check_url_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check appname args
        appname = kwargs.get("appname")

        if appname not in MONGO_CONFIG:
            return json_response_error(
                PARAM_ERROR, msg="appname error, check url")

        # check modelName args
        modelName = kwargs.get("modelName")
        if modelName:
            MODELNAME = get_model_cls(modelName)
            if not MODELNAME:
                return json_response_error(
                    PARAM_ERROR, msg="invalid modelname: %s" % modelName)

        return func(*args, **kwargs)
    return wrapper


def perf_logging(func):
    """
    Record the performance of each method call.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        urlpath = request.path
        remote_addr = request.remote_addr
        try:
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            proc_time = round(end_time - start_time, 3)
            _LOGGER.info('%s|%s|%s s.', urlpath, remote_addr, proc_time)
        except Exception as e:
            end_time = time.time()
            proc_time = round(end_time - start_time, 3)
            _LOGGER.error('%s error in %s s.', urlpath, proc_time)
            raise e
        return ret
    return wrapper
