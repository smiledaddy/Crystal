# -*- coding:utf-8 -*-
import logging

from rule_console.model.refered_info import ReferInfo


_LOGGER = logging.getLogger(__name__)


def add_refered_info(
        appname, target_field, target_id, refered_data, old_id=None):
    cond = {"target_id": int(target_id)}
    cond["target_field"] = target_field
    refer_info = ReferInfo.find_one(appname, cond, None)
    if not refer_info:
        refered_list = []
        refered_list.append(refered_data)
        info_instance = ReferInfo.new(target_field, target_id, refered_list)
        ReferInfo.save(appname, info_instance)
    else:
        if refered_data not in refer_info["refered_info"]:
            refer_info["refered_info"].append(refered_data)
            refer_info.pop("_id")
            ReferInfo.update(appname, cond, refer_info)
            _LOGGER.info("update the id refer info:%s", target_id)
    if old_id is not None:
        if old_id == target_id:
            return
        old_cond = {}
        old_cond["target_id"] = int(old_id)
        old_cond["target_field"] = target_field
        old_info = ReferInfo.find_one(appname, old_cond, None)
        if not old_info:
            _LOGGER.error("refered id:%s not in db", old_id)
            return
        if not old_info.get("refered_info"):
            _LOGGER.info("update the id refer info:%s", old_id)
            return ReferInfo.remove(appname, {"target_id": old_info["_id"]})
        if refered_data in old_info["refered_info"]:
            old_info["refered_info"].remove(refered_data)
        if old_info["refered_info"]:
            old_info.pop("_id")
            ReferInfo.update(appname, old_cond, old_info)
        else:
            ReferInfo.remove(appname, {"target_id": old_id})
        _LOGGER.info("update the id refer info:%s", old_id)


def delete_refered_info(appname, target_field, target_id, unrefer_data):
    """
    deference  refered info
    """
    cond = {"target_id": int(target_id)}
    cond["target_field"] = target_field
    refer_info = ReferInfo.find_one(appname, cond, None)
    if not refer_info:
        _LOGGER.error("refered id:%s not in db", target_id)
        return
    if not refer_info.get("refered_info"):
        return ReferInfo.remove(appname, {"target_id": target_id})
    if unrefer_data in refer_info["refered_info"]:
        refer_info["refered_info"].remove(unrefer_data)
    if refer_info["refered_info"]:
        refer_info.pop("_id")
        ReferInfo.update(appname, cond, refer_info)
    else:
        ReferInfo.remove(appname, {"target_id": target_id})
    _LOGGER.info("update the id refer info:%s", target_id)
