# -*- coding:utf-8 -*-
import logging

from armory.marine.util import now_timestamp, unixto_string
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_ERROR
from rule_console import settings
from rule_console.view.common_support import get_model_cls
from rule_console.model.rule import Rule
from rule_console.utils.common import get_list_page_info, get_rule_filter_list
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)
from rule_console.model import ArmoryMongo


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT


def create(appname, MODELNAME, data):
    cond = {"title": data["title"]}
    if MODELNAME.find_one(appname, cond):
        return json_response_error(DUPLICATE_FIELD, msg="the title exist")

    info_instance = MODELNAME.new(data)
    MODELNAME.save(appname, info_instance)
    _LOGGER.info("add a new %s:%s", MODELNAME.model_name,  data["title"])

    # get added info
    info = MODELNAME.find_one(appname, cond, MODELNAME.fields)
    info = get_list_page_info(info)

    return json_response_ok(info)


def info_list(
        appname, modelName, cond, page=0, page_size=PAGE_SIZE, sort=None):
    info_cursor = modelName.find(appname, cond, None)
    if sort is not None:
        info_cursor = info_cursor.sort(sort)
    info_cursor = info_cursor.skip(page * page_size).limit(page_size)
    infos = []
    for item in info_cursor:
        item = get_list_page_info(item)
        infos.append(item)

    total = modelName.find(appname, cond).count()

    filters = {}
    if issubclass(modelName, Rule):
        filters = get_rule_filter_list(appname)

    data = {}
    data.setdefault("items", infos)
    data.setdefault("total", total)
    data.setdefault("filters", filters)
    return json_response_ok(data)


def info_get(appname, modelName, cond):
    MODELNAME = get_model_cls(modelName)
    info = MODELNAME.find_one(appname, cond, MODELNAME.fields)
    if not info:
        return json_response_error(PARAM_ERROR, msg="invalid param id")
    info["id"] = info.pop("_id")
    return json_response_ok(info)


def info_mod(appname, MODELNAME, data):
    info_id = data.pop("id")
    old_info = MODELNAME.find_one(appname, {"title": data["title"]})
    if old_info and old_info["_id"] != info_id:
        return json_response_error(PARAM_ERROR, msg="the title exist")

    cond = {"_id": info_id}
    info = MODELNAME.find_one(appname, cond, MODELNAME.fields)
    if not info:
        return json_response_error(PARAM_ERROR, "invalid id: %s" % info_id)

    data["last_modified"] = now_timestamp()
    MODELNAME.update(appname, cond, data)
    _LOGGER.info("update %s:%s success", MODELNAME.model_name, info_id)

    data["last_modified"] = unixto_string(data.get("last_modified"))
    data["id"] = info_id
    return json_response_ok(data)


def info_del(appname, modelName, ids):
    MODELNAME = get_model_cls(modelName)
    data = {"success": [], "failed": []}
    for id in ids:
        try:
            id = int(id) if not isinstance(id, int) else id
        except:
            _LOGGER.info("id:%s type error", id)
            continue
        cond = {"_id": id}
        info = MODELNAME.find_one(appname, cond, None)
        if not info:
            _LOGGER.info("id %s is not exist", id)
            continue
        refer_cond = {}
        refer_cond[modelName] = id
        refer_rule = Rule.find(appname, refer_cond, toarray=True)
        if refer_rule:
                _LOGGER.info("id %s is refered", id)
                refer_info = {"id": id, "refered_info": []}
                for item in refer_rule:
                    temp_dict = {"modelName": "rule"}
                    temp_dict["id"] = item.get("_id")
                    refer_info["refered_info"].append(temp_dict)
                data["failed"].append(refer_info)
        else:
            MODELNAME.remove(appname, cond)
            data["success"].append({"id": id})

    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="delete successfully")


def get_package_display_data(appname):
    display_data = {}
    sort = [("last_modified", -1)]
    display_cursor = ArmoryMongo[appname]["platform"].find({}).sort(sort)
    display_list = []
    for item in display_cursor:
        item_dict = {}
        item_dict["display_value"] = item.get("title")
        item_dict["value"] = item.get("_id")
        display_list.append(item_dict)
    display_data["platform"] = display_list
    return json_response_ok(display_data, msg="")
