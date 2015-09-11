# -*- coding:utf-8 -*-
import logging
from werkzeug.wrappers import Response

from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.access_control import access_control, exception_handler
from armory.marine.respcode import PARAM_ERROR
from resource_console.api import request, app
from resource_console.model.icon import Icon
from resource_console.view.icon import (mod_icon, get_icon_display_data,
                        list_icon, create_icon, icon_get, del_from_admin)
from resource_console.settings import MONGO_CONFIG
from resource_console.utils.common import (
    get_list_cond, get_params, check_server_params, check_id_params)

_LOGGER = logging.getLogger(__name__)

API_GET_ICON = '/<appname>/resource/v1/icon/list'
API_GET_DISPLAYDATA = '/<appname>/resource/v1/icon/getDisplayData'
API_ADD_ICON = '/<appname>/resource/v1/icon/add'
API_EDIT_ICON = '/<appname>/resource/v1/icon/edit'
API_UPDATE_ICON = '/<appname>/resource/v1/icon/update'
API_DELETE_ICON = '/<appname>/resource/v1/icon/delete'


@app.route(API_GET_ICON, methods=['GET', ])
@exception_handler
@access_control
def icon_list(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    cond = get_list_cond(appname, request)
    sort = [("last_modified", -1)]
    return list_icon(appname, cond, index, limit, sort)


@app.route(API_GET_DISPLAYDATA, methods=['GET', ])
@exception_handler
@access_control
def get_displaydata(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    data = {}
    data["platform"] = get_icon_display_data(appname)
    return json_response_ok(data, msg="")


@app.route(API_ADD_ICON, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_icon_info(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    data = request.form
    new_data = get_params(Icon.params, data)
    new_data["icon"] = request.files.get('icon')

    return create_icon(appname, new_data)


@app.route(API_EDIT_ICON, methods=['GET', ])
@exception_handler
@access_control
def edit_icon_info(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    args = check_id_params(request)
    if isinstance(args, Response):
        return args
    return icon_get(appname, args)


@app.route(API_UPDATE_ICON, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_icon_info(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    args = check_id_params(request)
    if isinstance(args, Response):
        return args
    data = request.form
    new_data = get_params(Icon.params, data)
    new_data["icon"] = request.files.get('icon')
    return mod_icon(appname, args, new_data)


@app.route(API_DELETE_ICON, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_icon(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error")
    args = check_server_params(request)
    if isinstance(args, Response):
        return args

    # delete logic
    return del_from_admin(appname, args["items"])
