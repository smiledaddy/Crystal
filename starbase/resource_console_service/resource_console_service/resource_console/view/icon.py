# -*- coding:utf-8 -*-
import logging
import os
from multiprocessing.dummy import Pool as ThreadPool


from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.util import now_timestamp, unixto_string
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from resource_console.model.icon import Icon
from resource_console.utils.common import (save_icon_file, remove_icon_file)
from resource_console.utils.file_transfer import FileTransfer
from resource_console.model import ArmoryMongo
from resource_console import settings
from resource_console.utils.respcode import (
    DUPLICATE_DELETE, DUPLICATE_FIELD, DATA_RELETED_BY_OTHER)


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT
MEDIA_ROOT = settings.MEDIA_ROOT
_ICON_BASE_DIR = "icon/"


def list_icon(appname, cond,  page=0, page_size=PAGE_SIZE, sort=None):
    icon_cursor = Icon.find(appname, cond, None)
    if sort is not None:
        icon_cursor = icon_cursor.sort(sort)
    icon_cursor = icon_cursor.skip(
        page * page_size).limit(page_size)
    total = Icon.find(appname, cond).count()
    icons = []
    for item in icon_cursor:
        item["id"] = item.pop("_id")
        icons.append(item)
    filters = get_icon_filters(appname)
    data = {}
    data.setdefault("items", icons)
    data.setdefault("total", total)
    data.setdefault("filters", filters)
    return json_response_ok(data)


def create_icon(appname, data):
    for key in Icon.params:
        if not data.get(key):
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)

    # if not check_ospn_params(appname, data):
    #     return json_response_error(
    #         PARAM_ERROR, msg="param:platform or package error")

    data["title"] = "%s_%s" % (data["title"], now_timestamp())
    icon_info = Icon.find_one(appname, {"title": data["title"]})
    if icon_info:
        return json_response_error(
            DUPLICATE_FIELD, msg="the icon title exist")

    # save icon file to local file system
    data["icon"], data["height"], data["width"] = save_icon_file(
        data["icon"], appname)
    data["icon"] = _ICON_BASE_DIR + appname + '/' + data["icon"]

    # upload icon to file server
    file_path = os.path.join(MEDIA_ROOT, data["icon"])
    file_transfer = FileTransfer(file_path)
    data["guid"], data["download_url"] = file_transfer.start()

    # insert icon dict to database 
    icon_instance = Icon.new(data)
    Icon.save(appname, icon_instance)
    _LOGGER.info("add a new icon:%s", data["title"])

    icon_info = Icon.find_one(appname, {"title": data["title"]}, None)
    icon_info["id"] = icon_info.pop("_id")
    return json_response_ok(icon_info)


def icon_get(appname, iconid):
    cond = {"_id": iconid}
    icon = Icon.find_one(appname, cond, Icon.fields)
    if not icon:
        return json_response_error(PARAM_ERROR, msg='%s not in db' % (iconid))
    icon["id"] = icon.pop("_id")
    icon["last_modified"] = unixto_string(icon.get("last_modified"))
    return json_response_ok(icon)


def mod_icon(appname, icon_id, data):
    cond = {"_id": icon_id}
    icon = Icon.find_one(appname, cond, Icon.fields)
    if not icon:
        return json_response_error(PARAM_ERROR, msg='%s not in db' % icon_id)

    is_modified = True
    if data.get("icon") is None:
        data["icon"] = icon["icon"]
        is_modified = False

    for key in Icon.params:
        if not data.get(key):
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)

    # if not check_ospn_params(appname, data):
    #     return json_response_error(
    #         PARAM_ERROR, msg="param:platform or package error")

    icon_info = Icon.find_one(appname, {"title": data["title"]})
    if icon_info and icon_info["_id"] != icon_id:
        return json_response_error(DUPLICATE_FIELD, msg="the title exist")

    if is_modified:
        # remove old icon
        remove_icon_file(appname, icon["icon"])

        # save new icon
        data["icon"], data["height"], data["width"] = save_icon_file(
            data["icon"], appname)
        data["icon"] = _ICON_BASE_DIR + appname + '/' + data["icon"]

        # upload new icon to file server
        file_path = os.path.join(MEDIA_ROOT, data["icon"])
        file_transfer = FileTransfer(file_path)
        data["guid"], data["download_url"] = file_transfer.start()

        # update to database
        data["last_modified"] = now_timestamp()
        Icon.update(appname, cond, data)
        _LOGGER.info("update icon:%s success", icon_id)

    data["id"] = icon_id
    return json_response_ok(data)


def del_from_admin(appname, icon_ids):
    data = {"success": [], "failed": []}
    for icon_id in icon_ids:
        icon_id = int(icon_id) if not isinstance(icon_id, int) else icon_id
        cond = {"_id": icon_id}
        icon = Icon.find_one(appname, cond, None)
        if not icon:
            _LOGGER.info("icon id %s is not exist" % icon_id)
            continue
        if icon["refered_info"]:
            _LOGGER.info("icon id %s is refer" % icon_id)
            refer_info = {"id":  icon_id, "refered_info": []}
            refer_info["refered_info"] = icon["refered_info"]
            data["failed"].append(refer_info)
        else:
            # remove from database
            Icon.remove(appname, cond)
            # remove from filesystem 
            remove_icon_file(appname, icon["icon"])
            data["success"].append({"id": icon_id})
    if data["failed"]:
        return json_response_error(
            DATA_RELETED_BY_OTHER, data, msg="releted by other")
    else:
        return json_response_ok(data)


def get_icon_display_data(appname):
    sort = [("last_modified", -1)]
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

    return info


def get_icon_filters(appname):
    filters = []
    sort = [("last_modified", -1)]
    fields = {"_id": 1, "title": 1}
    info = {"name": "platform", "items": []}
    platform_cursor = ArmoryMongo[appname]["platform"].find(
        {}, fields).sort(sort)
    for os_item in platform_cursor:
        plat_dict = {"display_value": "", "value": ""}
        plat_dict["value"] = os_item.get("_id")
        plat_dict["display_value"] = os_item.get("title")
        info["items"].append(plat_dict)
    default = {"display_value": u"选择平台", "value": "all"}
    info["items"].insert(0, default)
    filters.append(info)

    return filters


# deprecated
def check_ospn_params(appname, data):
    try:
        platform = int(data.get("platform"))
    except:
        _LOGGER.error("param:platform type error")
        return False
    platform_cursor = ArmoryMongo[appname]["platform"].find_one(
        {"_id": platform})
    if not platform_cursor:
        return False
    pn_ids = data.get("package")
    try:
        pn_ids = [int(item) for item in pn_ids]
    except:
        _LOGGER.error("param:platform type error")
        return False
    for pn_id in pn_ids:
        pn = ArmoryMongo[appname]["package"].find_one(
            {"_id": pn_id, "platform": platform})
        if not pn:
            return False
    return True
