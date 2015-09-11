# -*- coding: utf-8 -*-
import logging
import redis
import cPickle as pickle


_LOGGER = logging.getLogger("multalisk")
_EXPIRE_TIME = 3600


cache = None


def init_cache(host='127.0.0.1', port=6379):
    global cache
    cache = redis.Redis(host, port, charset='utf-8', db=1)


def get_search_obj(db_type, model_class, search_q):
    try:
        cache_key = "multalisk:%s:%s:%s" % (db_type, model_class, search_q)
        cache_obj = cache.get(cache_key)
        return pickle.loads(cache_obj) if cache_obj else None
    except Exception as e:
        _LOGGER.error('cache error when get search obj, error:%s' % e)


def set_search_obj(db_type, model_class, search_q, search_obj):
    try:
        cache_key = "multalisk:%s:%s:%s" % (db_type, model_class, search_q)
        cache_obj = pickle.dumps(search_obj, True)
        cache.set(cache_key, cache_obj)
        cache.expire(cache_key, _EXPIRE_TIME)
    except Exception as e:
        _LOGGER.error('cache error when set search obj, error:%s' % e)


def get_filter_obj(filter_dict):
    try:
        cache_key = "multalisk:filters:%s" % filter_dict
        cache_obj = cache.get(cache_key)
        return pickle.loads(cache_obj) if cache_obj else None
    except Exception as e:
        _LOGGER.error('cache error when get filters obj, error:%s' % e)


def set_filter_obj(filter_dict, filter_obj):
    try:
        cache_key = "multalisk:filters:%s" % filter_dict
        cache_obj = pickle.dumps(filter_obj, True)
        cache.set(cache_key, cache_obj)
        cache.expire(cache_key, _EXPIRE_TIME)
    except Exception as e:
        _LOGGER.error('cache error when set filter obj, error:%s' % e)
