# -*- coding: utf-8 -*-
import logging
import time
import simplejson
from uuid import uuid4
from functools import wraps
from pymongo import MongoClient
from pylon.frame import make_response

from armory.marine.json_rsp import json_response_error
from auth_service.settings import MONGO_CONFIG
from armory.marine.respcode import PARAM_ERROR
from auth_service.settings import NAV_DICT
from auth_service.api import request
from auth_service.model.apps import App
from auth_service.model.module import Module


_LOGGER = logging.getLogger(__name__)


def check_url_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check projectname args
        projectname = kwargs.get("projectname")
        if projectname:
            if projectname not in NAV_DICT.keys():
                return json_response_error(
                    PARAM_ERROR, msg="invalid projectname: %s" % projectname)

        # check appname args
        appname = kwargs.get("appname")
        if appname not in MONGO_CONFIG:
            return json_response_error(
                PARAM_ERROR, msg="appname error, check url")

        # check applabel args
        applabel = kwargs.get("applabel")
        if applabel:
            app_cond = {'name': applabel, "app_name": projectname}
            if not App.find_one(appname, app_cond):
                return json_response_error(
                    PARAM_ERROR, msg="the app label not exist")

        # check module args
        module = kwargs.get("module")
        if module:
            module_cond = {'module_name': module, "app_name": projectname}
            if not Module.find_one(appname, module_cond):
                return json_response_error(
                    PARAM_ERROR, msg="the app module not exist")

        # check id args
        id = kwargs.get("id")
        if id:
            try:
                id = int(id)
            except ValueError:
                return json_response_error(PARAM_ERROR, msg="id error")
        return func(*args, **kwargs)
    return wrapper


def save_sesson(save_dict={}, host='localhost', port=27017, db='', col=''):
    client = MongoClient(host, port)
    session_store = client[db][col]
    time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    save_dict.update({'create': time_str})
    sid = save_dict.get('sid', str(uuid4()))
    session_store.update({'sid': sid}, save_dict, True)


def get_response_info(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        resp = make_response(func(*args, **kwargs))
        data = resp.data
        try:
            res_d = simplejson.loads(data)
            user_info = res_d.get('data')
            save_dict = {}
            if user_info:
                uid = user_info.get('uid')
                sid = str(uuid4())
                resp.set_cookie('sessionid', sid)
                remote_ip = request.remote_addr
                save_dict = {
                    'sid': sid,
                    'uid': uid,
                    'remote_ip': remote_ip}
                save_sesson(save_dict, db='usermanage', col='sessions')
        except Exception as e:
            _LOGGER.error('responed data error %s' % e)
        return resp
    return decorated_function
