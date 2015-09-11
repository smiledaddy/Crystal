# -*- coding: utf-8 -*-
import logging
import os

from armory.marine.util import now_timestamp
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_ERROR
from auth_service.model.checklist import CheckList
from auth_service.utils.common import update_status_by_id
from auth_service.model.right import Right
from auth_service.model.group import Group
from auth_service.model.user import User
from auth_service.view.user import user_info
from auth_service import settings
from auth_service.utils.common import (
    send_email, get_module_value, get_project_value)

_LOGGER = logging.getLogger(__name__)
TEMPLATE_ROOT = settings.CUS_TEMPLATE_DIR


def checklist_create(appname, projectname, applabel, module, uid, ids):
    '''
    this api to add checklist.
    Request URL: /<projectname>/auth/<applabel>/<modulename>/submit
    Parameters:
    {
        'app_name': 'homeadmin',
        'module_name': 'banner',
        'items': [1, 2, 3]
    }
    '''
    data = {"success": [], "failed": []}
    check_uids = []
    check_uids = get_check_uids(appname, projectname, applabel, module)
    ids = [int(id) for id in ids]
    for id in ids:
        info = update_status_by_id(appname, projectname, module, id, 1)
        if not info:
            data["failed"].append(id)
            continue
        cond = {
            "check_id": id, 'projectname': projectname, "submit_uid": uid,
            "app_name": applabel, "module_name": module}
        old_check_info = CheckList.find_one(appname, cond, {"_id": 0})
        if old_check_info:
            old_check_info["status"] = 1
            old_check_info["mark"] = ""
            old_check_info["check_uid"] = check_uids
            old_check_info["last_modified"] = now_timestamp()
            CheckList.update(appname, cond, old_check_info)
        else:
            checklist_instance = CheckList.new(
                projectname, applabel, module, id, uid, check_uids)
            CheckList.save(appname, checklist_instance)
        data["success"].append(info)
    _send_email_to_assessor(appname, projectname, module, uid, check_uids, ids)
    if data["failed"]:
        return json_response_error(PARAM_ERROR, data, msg="invalid id")
    return json_response_ok(data)


def check_content(appname, projectname, applabel, module, id, data):
    '''
    this api is used to check content
    Request URL: /<projectname>/auth/<applabel>/<modulename>/check/<id>
    HTTP Method: POST
    Parameters:
        {
            "checked": 3,
            "mark": ""
        }
    Return:
     {
        "status":0
        "data":{
            "id": 1,
            "checked": 3,
            "release": 1,
            "last_modified": "2015-04-16 14:10:37"
            }
        "msg":""
     }
    '''
    id = int(id)
    cond = {
        "check_id": id, 'projectname': projectname, "check_uid": data["uid"],
        "app_name": applabel, "module_name": module}
    check_info = CheckList.find_one(appname, cond, None)
    if not check_info:
        _LOGGER.info("check info id %s is not submit" % id)
        return json_response_error(
            PARAM_ERROR, data, msg="invalid id, %s is not submit" % id)

    #update response info in coll
    info = update_status_by_id(
        appname, projectname, module, id, data["checked"])
    if not info:
        return json_response_error(
            PARAM_ERROR, data, msg="invalid id,check parameters")

    #update check list
    data["last_modified"] = now_timestamp()
    CheckList.update(appname, cond, data)
    _send_email_to_user(
        appname, projectname, module, data["uid"], check_info["submit_uid"],
        id, data["mark"])
    return json_response_ok(info)


def get_check_uids(
        appname, projectname, applabel, module,
        action="checked", perm_lc="all"):
    # get perm id
    perm_name = '%s-%s-%s' % (applabel, module, action)
    right_cond = {
        'perm_name': perm_name, 'app_name': projectname, "lc": perm_lc}
    perm = Right.find_one(appname, right_cond)
    if not perm:
        _LOGGER.error("the right:%s not exist" % perm_name)
    #get user who has this right
    check_ids = []
    perm_id = perm["_id"]
    perm_key = "permission_list.%s" % projectname
    group_cond = {perm_key: perm_id}
    groups_info = Group.find(appname, group_cond)
    group_ids = [i["_id"] for i in groups_info]
    for gid in group_ids:
        group_info = user_info(appname, gid)
        user_ids = [i["id"] for i in group_info]
        check_ids += user_ids

    user_cond = {perm_key: perm_id}
    users_info = User.find(appname, user_cond)
    user_ids = [i["_id"] for i in users_info]
    check_ids += user_ids
    check_ids = list(set(check_ids))
    return check_ids


def _send_email_to_assessor(appname, projectname, module, uid, uids, ids):
    subject = u"Submit check list"
    from_info = User.find_one(appname, {"_id": uid}, {"user_name": 1})
    from_to = from_info.get("user_name")
    mail_to = []
    for uid in uids:
        user_info = User.find_one(
            appname, {"_id": uid}, {"user_name": 1, "_id": 0})
        mail_to.append(user_info.get("user_name"))
    mail_to.append("yqyu@bainainfo.com")
    template = os.path.join(TEMPLATE_ROOT, "submit_checklist.html")
    module = get_module_value(appname, projectname, module)
    projectname = get_project_value(projectname)
    send_email(subject, template, mail_to, from_to, projectname, module, ids)


def _send_email_to_user(
        appname, projectname, module, uid, submit_uid, id, mark):
    user_info = User.find_one(
        appname, {"_id": submit_uid}, {"user_name": 1, "_id": 0})
    subject = u"Check result"
    template = os.path.join(TEMPLATE_ROOT, "check_info.html")
    mail_to = [user_info.get("user_name")]
    from_to = User.find_one(
        appname, {"_id": uid}, {"user_name": 1}).get("user_name")
    mail_to.append("yqyu@bainainfo.com")
    module = get_module_value(appname, projectname, module)
    projectname = get_project_value(projectname)
    send_email(
        subject, template, mail_to, from_to, projectname, module, id, mark)
