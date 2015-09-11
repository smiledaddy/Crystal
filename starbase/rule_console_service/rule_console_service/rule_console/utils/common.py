# -*- coding: utf-8 -*-
import logging
import re
import time

from armory.marine.util import unixto_string
from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_error
from armory.marine.respcode import PARAM_ERROR, PARAM_REQUIRED
from rule_console.model import ArmoryMongo

_ONE_DAY = 86400.0
PARAM_OPTION_LIST = ["need", 'noneed', 'option']
_RULE_FILTER_KEY = ['platform', 'package', 'locale']
_LOGGER = logging.getLogger(__name__)


def get_list_cond(appname, request, module):
    os = request.args.get("platform", "all")
    pn = request.args.get("package", "all")
    lc = request.args.get("locale", "all")
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    searchKeyword = request.args.get("searchKeyword")
    cond = {}
    if start_time and end_time:
        start = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
        end = time.mktime(time.strptime(end_time, '%Y-%m-%d')) + _ONE_DAY
        cond["last_modified"] = {"$gte": start, "$lte": end}
    if os != "all":
        cond["platform"] = int(os)
    if pn != "all":
        cond["package"] = int(pn)
    if lc != "all":
        cond["locale"] = int(lc)
    if searchKeyword:
        cond = search_cond(searchKeyword, module.search_fields)
    return cond


def get_list_page_info(item):
    item["id"] = item.pop("_id")
    item["first_created"] = unixto_string(item.get("first_created"))
    item["last_modified"] = unixto_string(item.get("last_modified"))
    return item


def get_rule_filter_list(appname):
    filter_list = []
    sort = [("last_modified", -1)]
    for filter_item in _RULE_FILTER_KEY:
        filter_dict = {"items": [], "name": filter_item}
        filter_cursor = ArmoryMongo[appname][filter_item].find({}).sort(sort)
        for item in filter_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            filter_dict['items'].append(item_dict)
        if filter_item == "package":
            default = {"display_value": u"项目名称", "value": "all"}
        elif filter_item == "locale":
            default = {"display_value": u"选择Locales", "value": "all"}
        else:
            default = {"display_value": u"选择平台", "value": "all"}
        filter_dict["items"].insert(0, default)
        filter_list.append(filter_dict)

    return filter_list


def search_cond(search_keyword, search_fields):
    cond = {}
    regex_cond_list = []
    for key in search_fields.keys():
        regex_cond = {}
        if search_fields.get(key)["data_type"] == "int":
            try:
                regex_cond[key] = int(search_keyword)
            except:
                _LOGGER.error("not a number string")
        elif search_fields.get(key)["data_type"] == "string":
            regex_cond[key] = {"$regex": re.escape(search_keyword)}
        if regex_cond:
            regex_cond_list.append(regex_cond)
    if regex_cond_list:
        cond["$or"] = regex_cond_list
    return cond


def _conv(func):
    def wrapper(*args, **kwargs):
        if func == bool:
            return bool(int(*args, **kwargs))
        return func(*args, **kwargs)
    return wrapper


def get_valid_params(request, keys):
    '''
    get valid params by params rule
    '''
    if request.method == "GET":
        query_dict = request.args
    elif request.method == "POST":
        try:
            query_dict = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("post para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
    result = {}
    for key in keys:
        paras = key.split('&')
        paras = paras[:4]
        (param_key, param_option, param_type, default_value) = tuple(paras) \
            + (None,) * (4 - len(paras))
        if not param_key or param_option not in PARAM_OPTION_LIST:
            # invalid config for parameter %key%
            continue
        param_value = query_dict.get(param_key)

        if param_value is None:
            if param_option == 'need':
                return json_response_error(
                    PARAM_REQUIRED, msg="no param:%s" % param_key)
            if param_option == 'noneed':
                continue
            if default_value is not None:
                param_value = _conv(eval(param_type))(default_value)
            else:
                param_value = default_value
        else:
            if param_type is not None:
                try:
                    param_value = _conv(eval(param_type))(param_value)
                except Exception as e:
                    return json_response_error(
                        PARAM_ERROR, msg="param:%s type error" % param_key)
        result[param_key] = param_value
    return result


def check_rule_params(appname, query_dict, keys):
    # check id of pn/op/src/lc
    for arg in keys:
        try:
            query_dict[arg] = list(set([int(i) for i in query_dict[arg]]))
        except:
            return json_response_error(
                PARAM_ERROR, msg="param:%s type error" % arg)
        arg_id = query_dict[arg]
        if arg == "package":
            if not arg_id:
                return json_response_error(
                    PARAM_ERROR, msg="parameters:package error")
        if arg_id:
            for item in arg_id:
                arg_cond = {"_id": item}
                if arg == "package":
                    arg_cond["platform"] = query_dict.get("platform")
                if not ArmoryMongo[appname][arg].find_one(arg_cond):
                    return json_response_error(
                        PARAM_ERROR, msg="parameters:%s id error" % arg)
    return query_dict
