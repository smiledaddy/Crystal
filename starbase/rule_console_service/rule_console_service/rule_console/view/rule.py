# -*- coding:utf-8 -*-
import logging


from armory.marine.json_rsp import json_response_ok, json_response_error
from rule_console.model.rule import Rule
from rule_console.model.refered_info import ReferInfo
from rule_console.model import ArmoryMongo
from rule_console.utils.respcode import DATA_RELETED_BY_OTHER

_LOGGER = logging.getLogger(__name__)
_RULE_DISPLAY_KEY = ['operator', 'source', 'locale']


def get_rule_display_data(appname):
    display_data = {}
    sort = [("title", 1), ("_id", 1)]

    # get operator/source/locale info list
    for display_item in _RULE_DISPLAY_KEY:
        display_cursor = ArmoryMongo[appname][display_item].find(
            {}).sort(sort)
        display_list = []
        for item in display_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            display_list.append(item_dict)
        display_data[display_item] = display_list

    # get platform and package info linkage control dict
    fields = {"_id": 1, "title": 1}
    info = {"name": "platform", "items": []}
    platform_cursor = ArmoryMongo[appname]["platform"].find(
        {}, fields).sort(sort)
    for os_item in platform_cursor:
        plat_dict = {"display_value": "", "value": "", "children": {}}
        plat_dict["value"] = os_item.get("_id")
        plat_dict["display_value"] = os_item.get("title")
        plat_child = {"name": "package", "items": []}
        cond = {"platform": os_item["_id"]}
        package_cursor = ArmoryMongo[appname]["package"].find(
            cond, fields).sort(sort)
        for item in package_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            plat_child["items"].append(item_dict)
        plat_dict["children"] = plat_child
        info["items"].append(plat_dict)
    display_data["platform"] = info

    return json_response_ok(display_data)


def delete_rule_info(appname, rule_ids):
    data = {"success": [], "failed": []}
    for rule_id in rule_ids:
        try:
            rule_id = int(rule_id) if not isinstance(rule_id, int) else rule_id
        except:
            _LOGGER.error("id:%s type error", rule_id)
            continue

        cond = {"_id": rule_id}
        rule = Rule.find_one(appname, cond, None)
        if not rule:
            _LOGGER.error("rule id %s is not exist", rule_id)
            continue
        refer_cond = {"target_id": int(rule_id), "target_field": "rule"}
        refer_rule = ReferInfo.find_one_refered_info(
            appname, refer_cond, None)
        if refer_rule:
            _LOGGER.info("rule id %s is refer", rule_id)
            refer_info = {"id": rule_id}
            refer_info["refered_info"] = refer_rule["refered_info"]
            data["failed"].append(refer_info)
        else:
            Rule.remove(appname, cond)
            data["success"].append({"id": rule_id})

    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="delete successfully")
