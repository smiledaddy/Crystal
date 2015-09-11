# -*- coding: utf-8 -*-
import logging

from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_error
from armory.marine.mail import MailSender
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from armory.marine.util import now_timestamp, unixto_string
from auth_service.model import ArmoryMongo
from auth_service.settings import NAV_DICT
from auth_service.model.module import Module

_LOGGER = logging.getLogger(__name__)


def get_params(params, data):
    new_data = {}
    for key in params:
        new_data[key] = data[key]
    return new_data


def check_required_params(request, params):
    if request.method == "GET":
        data = request.args
    elif request.method == "POST":
        try:
            data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
    for key in params:
        if key not in data:
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)
    new_data = get_params(params, data)
    return new_data


def get_coll_by_module(appname, projectname, modulename):
    cond = {
        "projectname": projectname,
        "modulename": modulename}
    coll_info = ArmoryMongo[appname]["module_map"].find_one(cond)
    if coll_info:
        return coll_info["coll"]
    else:
        return None


def update_status_by_id(appname, projectname, modulename, id, status):
    coll = get_coll_by_module(appname, projectname, modulename)
    cond = {"_id": id}
    field = {
        "_id": 0, "checked": 1, "last_modified": 1,
        "upload_local": 1, "upload_ec2": 1}
    info = ArmoryMongo[projectname][coll].find_one(cond, field)
    if info:
        info["checked"] = status
        info["last_modified"] = now_timestamp()
        ArmoryMongo[projectname][coll].update(cond, {'$set': info})
        info["release"] = get_status(info)
        info["last_modified"] = unixto_string(info["last_modified"])
        info["id"] = id
        return info
    else:
        return None


def get_status(item):
    if item["last_modified"] > item["upload_local"]:
        release = 1
    elif item["last_modified"] < item["upload_local"] and \
            item["last_modified"] > item["upload_ec2"]:
        release = 2
    else:
        release = 0
    return release


def send_email(subject, template, to_list, *args):
    mail_sender = MailSender.getInstance()
    mail_sender.init_conf({
        'server': '172.16.255.214:465',
        'user': 'i18nStudio@baina.com',
        'passwd': 'i18P@55word',
        'from': 'I18N Studio<i18nStudio@bainainfo.com>',
        'to': []
    })
    try:
        f = open(template, 'r')
        s = f.read()
        html_str = s % args
        mail_sender.send(subject, html_str, to_list)
    except Exception, e:
        _LOGGER.error("read file and format occurred exception:%s" % e)


def get_project_value(project):
    return NAV_DICT.get(project)


def get_module_value(appname, projectname, module_name):
    cond = {"module_name": module_name, "app_name": projectname}
    fields = {"module_value": 1}
    module = Module.find_one(appname, cond, fields)
    return module.get("module_value")
