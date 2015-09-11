#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (c) 2012 Baina Info Inc. All rights reserved.
# Created On Mar 7, 2013
# @Author : Jun Wang
# Email: jwang@bainainfo.com
import subprocess
import logging
import os
import re
import time
from PIL import Image
import simplejson
import errno
import shutil

from armory.marine.util import now_timestamp
from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from resource_console import settings

_LOGGER = logging.getLogger(__name__)


_ONE_DAY = 86400.0
MEDIA_ROOT = settings.MEDIA_ROOT
_ICON_BASE_DIR = "icon/"


def sdel(hosts, user, key_file, remote):
    servers = ['%s@%s' % (user, ip) for ip in hosts]
    for server in servers:
        sdel_file = 'ssh -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s "rm %s"' % (key_file, server, remote)
        _LOGGER.debug(sdel_file)
        try:
            result = subprocess.call(sdel_file, shell=True)
            if result != 0:
                _LOGGER.error(result)
            _LOGGER.info(result)
        except Exception, e:
            _LOGGER.exception(e)
            return False
    return True


def scp(hosts, user, key_file, local, remote):
    remote_dir = os.path.dirname(remote)
    servers = ['%s@%s' % (user, ip) for ip in hosts]
    for server in servers:
        mkdir = 'ssh -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s "mkdir -p %s"' % (key_file, server, remote_dir)
        scp_file = 'scp -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s %s:%s' % (key_file, local, server, remote)
        _LOGGER.debug(scp_file)
        try:
            result = subprocess.call(scp_file, shell=True)
            if result != 0:
                dir_result = subprocess.call(mkdir, shell=True)
                if dir_result != 0:
                    _LOGGER.error(dir_result)
                    return False
                result = subprocess.call(scp_file, shell=True)
            _LOGGER.info(result)
            if result != 0:
                return False
        except Exception, e:
            _LOGGER.exception(e)
            return False
    return True


def search_cond(appname, search_keyword):
    cond = {}
    cond_list = []
    try:
        id_cond = {}
        id_cond["_id"] = int(search_keyword)
        cond_list.append(id_cond)
    except:
        _LOGGER.debug("not a number string")
    string_fields = ["title", ]
    for field in string_fields:
        string_cond = {}
        string_cond[field] = {
            "$regex": re.escape(search_keyword),  '$options': '$i'}
        cond_list.append(string_cond)
    cond["$or"] = cond_list
    return cond


def get_list_cond(appname, request):
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    searchKeyword = request.args.get("searchKeyword")
    platform = request.args.get("platform", "all")
    cond = {}
    if searchKeyword:
        cond = search_cond(appname, searchKeyword)
    if start_time and end_time:
        start = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
        end = time.mktime(time.strptime(end_time, '%Y-%m-%d')) + _ONE_DAY
        cond["last_modified"] = {"$gte": start, "$lte": end}
    if platform != "all":
        cond["platform"] = int(platform)
    return cond


def get_params(params, data):
    new_data = {}
    for key in params:
        new_data[key] = data.get(key)
        if key == "type" or key == "package":
            new_data[key] = simplejson.loads(new_data[key])
        elif key == "platform":
            new_data[key] = int(new_data[key])
    return new_data


def save_icon_file(iconfile, appname):
    # save icon file to resource path
    icon_name = iconfile.filename.lower()
    icon_suffix = icon_name.split('.')[-1]
    icon_name = "%s.%s" % (now_timestamp(), icon_suffix)
    icon_path = os.path.join(MEDIA_ROOT, _ICON_BASE_DIR, appname)
    if not os.path.exists(icon_path):
        os.makedirs(icon_path)
    iconfilepath = os.path.join(icon_path, icon_name)
    iconfile.save(iconfilepath)

    # get icon file height and width
    try:
        image = Image.open(iconfilepath)
        height, width = image.size
    except:
        height, width = (0, 0)
    return icon_name, height, width


def remove_icon_file(appname, iconfile):
    # remove icon file from resource path
    old_iconfilepath = os.path.join(MEDIA_ROOT, iconfile)
    if os.path.exists(old_iconfilepath):
        os.remove(old_iconfilepath)


def check_id_params(request):
    method = request.method
    if method == "GET":
        args = request.args
    elif method == "POST":
        args = request.form
    if 'id' not in args:
        return json_response_error(PARAM_REQUIRED, msg="not param:id")
    try:
        id = int(args["id"])
    except ValueError:
        return json_response_error(PARAM_ERROR, msg="id error")
    return id


def check_server_params(request):
    try:
        data = ArmoryJson.decode(request.data)
    except ValueError:
        return json_response_error(PARAM_ERROR, msg="json loads error")

    # check required args
    for key in ["items", "server"]:
        if key not in data:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % key)

    # check param: server
    if data["server"] not in ["local", "ec2", "admin"]:
        return json_response_error(PARAM_ERROR, msg="server param error")
    return data
