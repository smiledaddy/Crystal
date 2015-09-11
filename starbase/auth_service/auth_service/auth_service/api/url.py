# -*- coding:utf-8 -*-
import logging
import simplejson
from werkzeug.wrappers import Response


from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import (
    METHOD_ERROR, AUTH_ERROR, PARAM_ERROR)
from armory.marine.access_control import access_control, exception_handler
from auth_service.settings import NAV_DICT
from auth_service.api import request, session, app
from auth_service.view.user import (
    user_login, user_create, user_delete, user_list, user_mod, user_get,
    user_chpasswd, user_active, user_right_get, user_right_mod)
from auth_service.view.group import (
    group_create, group_delete, group_list, group_name_mod, group_get,
    get_role_display_data, group_right_get, group_right_mod)
from auth_service.view.right import (
    right_create, right_delete, right_list, right_mod, right_get,
    check_session, menu_list, navigate_list, get_right_display_data)
from auth_service.view.modules import (
    module_create, module_list, module_mod, module_get)
from auth_service.view.apps import (
    app_create, app_list, app_mod, app_get)
from auth_service.utils.common import check_required_params
from auth_service.decorator import check_url_params
from auth_service.model.user import User
from auth_service.model.group import Group
from auth_service.model.apps import App
from auth_service.model.module import Module
from auth_service.model.right import Right

from auth_service.decorator import get_response_info
from auth_service.userlog import save_loginfo, get_userlog
from auth_service.settings import MONGO_CONFIG


_LOGGER = logging.getLogger('auth_service')


# user log info
@app.route('/<appname>/loginfo', methods=['POST', 'OPTIONS'])
def savelog(appname):
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    try:
        data_obj = simplejson.loads(request.data)
        status = save_loginfo(data_obj)
        return json_response_ok(data={'status': status}, msg='response status')
    except ValueError as expt:
        _LOGGER.error("save log para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")


@app.route('/<appname>/userlog', methods=['GET', ])
@exception_handler
@access_control
def getlog(appname):
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    sort_dict = {}
    sort_strs = request.args.get('sort')
    if sort_strs:
        try:
            sort_dict = simplejson.loads(sort_strs)
        except ValueError, e:
            _LOGGER.error(e)
            return json_response_error(PARAM_ERROR, msg='sort string error')
    if sort_dict.get('sort_way') == 'id':
        sort_dict['sort_way'] = '_id'
    query = {
        'index': int(request.args.get('index', 1)) - 1,
        'limit': int(request.args.get('limit', 20)),
        'sort_field': sort_dict.get('sortBy', 'optime'),
        'sort_way': 1 if sort_dict.get('sortWay') == 'asc' else -1,
        'keyword': request.args.get('searchKeyword'),
        'start': request.args.get('start'),
        'end': request.args.get('end')}
    data = get_userlog(query)
    return json_response_ok(data, msg='get user log')


# login logout func
@app.route('/<appname>/login', methods=['POST', 'OPTIONS'])
@get_response_info
@exception_handler
@access_control
@check_url_params
def login(appname):
    required_list = ("user_name", "password")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return user_login(
        appname, data['user_name'], data['password'], session)


@app.route('/<appname>/logout', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def logout(appname):
    # logout remove uid from session
    session.pop('uid', None)
    # view logic
    return json_response_ok()


@app.route('/<appname>/changepwd', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def chpasswd_user(appname):
    if not session.get('uid'):
        _LOGGER.error('cant find uid in session')
        return json_response_error(AUTH_ERROR)
    required_list = ("current_password", "new_password")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    return user_chpasswd(
        appname, session.get('uid'), data['current_password'],
        data['new_password'])


# add user group right
@app.route('/<appname>/user/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def add_user(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ("user_name", "group_id")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    add_data = ArmoryJson.decode(request.data)
    data["mark"] = add_data.get("mark", "")
    # view logic
    return user_create(appname, data)


@app.route('/<appname>/group/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def add_group(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ("rolename", )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return group_create(appname, data['rolename'])


@app.route('/<appname>/<projectname>/perm/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def add_right(appname, projectname):
    required_list = ('perm_module', 'perm_opname', 'perm_action', "perm_type")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data

    action_value = ['list', 'add', 'edit', 'delete']
    if data["perm_type"] == "module" and \
            data["perm_action"] not in action_value:
        return json_response_error(PARAM_ERROR)
    perm_lc = request.form.get('perm_lc', "all")

    # view logic
    return right_create(
        appname, projectname, data["perm_module"], data["perm_opname"],
        data["perm_action"], data["perm_type"], perm_lc)


@app.route('/<appname>/<projectname>/module/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def add_module(appname, projectname):
    required_list = ('module_name', "module_value", "order")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return module_create(
        appname, projectname, data['module_name'],
        data["module_value"], data["order"])


@app.route('/<appname>/<projectname>/app/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def add_app(appname, projectname):
    required_list = ('name', "app_value", "order")
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return app_create(
        appname, projectname, data['name'], data["app_value"], data["order"])


# del user group right
@app.route('/<appname>/user/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def del_user(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ('uids', )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return user_delete(appname, data['uids'])


@app.route('/<appname>/group/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def del_group(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ('gids', )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data

    # view logic
    return group_delete(appname, data['gids'])


@app.route('/<appname>/right/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def del_right(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ('pids', )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    # view logic
    return right_delete(appname, data['pids'])


# list user group right
@app.route('/<appname>/user/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_user(appname):
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    searchKeyword = request.args.get("searchKeyword")
    return user_list(appname, index, limit, searchKeyword)


@app.route('/<appname>/user/getDisplayData', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def get_role_displaydata(appname):
    data = {}
    data["roles"] = get_role_display_data(appname)
    return json_response_ok(data, msg="")


@app.route('/<appname>/group/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_group(appname):
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    return group_list(appname, index, limit)


@app.route('/<appname>/perm/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_right(appname):
    return right_list(appname)


@app.route('/<appname>/<projectname>/menu/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_menu(appname, projectname):
    required_list = ('uid', )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    return menu_list(appname, projectname, data["uid"])


@app.route('/<appname>/navigate/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_navigate(appname):
    required_list = ('uid', )
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    return navigate_list(appname, data["uid"])


@app.route('/<appname>/label/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_label(appname):
    data = {}
    label = []
    app_names = NAV_DICT.keys()
    for app_name in app_names:
        app_dict = {}
        app_display = NAV_DICT.get(app_name)
        app_dict.setdefault("display_value", app_display)
        app_dict.setdefault("value", app_name)
        label.append(app_dict)
    data.setdefault("navigate", label)
    return json_response_ok(data, msg="")


@app.route('/<appname>/<projectname>/perm/getDisplayData', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def perm_display(appname, projectname):
    data = get_right_display_data(appname, projectname)
    return json_response_ok(data, msg="")


@app.route('/<appname>/module/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_module(appname):
    return module_list(appname)


@app.route('/<appname>/app/list', methods=['GET', ])
@exception_handler
@access_control
@check_url_params
def list_app(appname):
    return app_list(appname)


# get single user group right or mod user group right
@app.route('/<appname>/user/<id>', methods=['GET', 'POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def user_edit(appname, id):
    if request.method == 'GET':
        # this method get user info by uid
        return user_get(appname, int(id))
    elif request.method == 'POST':
        # this method mod user info
        data = check_required_params(request, User.params)
        if isinstance(data, Response):
            return data
        return user_mod(appname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/group/<id>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def group_info(appname, id):
    if request.method == 'GET':
        # this method get group info by gid
        return group_get(appname, int(id))
    elif request.method == 'POST':
        # this method mod group info
        data = check_required_params(request, Group.params)
        if isinstance(data, Response):
            return data
        return group_name_mod(appname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/module/<id>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def module_info(appname, id):
    if request.method == 'GET':
        # this method get group info by gid
        return module_get(appname, int(id))
    elif request.method == 'POST':
        # this method mod group info
        data = check_required_params(request, Module.params)
        if isinstance(data, Response):
            return data
        return module_mod(appname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/app/<id>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def app_info(appname, id):
    if request.method == 'GET':
        # this method get group info by gid
        return app_get(appname, int(id))
    elif request.method == 'POST':
        # this method mod group info
        data = check_required_params(request, App.params)
        if isinstance(data, Response):
            return data
        return app_mod(appname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/perm/<id>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def right_info(appname, id):
    if request.method == 'GET':
        # this method get group right info by gid
        return right_get(appname, int(id))
    elif request.method == 'POST':
        # this method mod group right info
        data = check_required_params(request, Right.params)
        if isinstance(data, Response):
            return data
        return right_mod(appname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route(
    '/<appname>/<projectname>/group/perm/<id>',
    methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def group_right_info(appname, projectname, id):
    if request.method == 'GET':
        # this method get group right info by gid
        return group_right_get(appname, projectname, int(id))
    elif request.method == 'POST':
        # this method mod group right info
        required_list = ("perm_list", )
        data = check_required_params(request, required_list)
        if isinstance(data, Response):
            return data
        return group_right_mod(appname, projectname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route(
    '/<appname>/<projectname>/user/perm/<id>',
    methods=['GET', 'POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def user_right_info(appname, projectname, id):
    if request.method == 'GET':
        # this method get right info by gid
        return user_right_get(appname, projectname, int(id))
    elif request.method == 'POST':
        # this method mod user right info
        required_list = ("perm_list", "disable_list")
        data = check_required_params(request, required_list)
        if isinstance(data, Response):
            return data
        return user_right_mod(appname, projectname, int(id), data)
    else:
        return json_response_error(METHOD_ERROR)


# verify right
@app.route('/<appname>/perm/check', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def auth_right(appname):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    required_list = ('perm_module', 'perm_opname', 'perm_action')
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    perm_lc = request.form.get('perm_lc', "all")
    return check_session(
        appname, data["perm_module"], data["perm_opname"],
        data["perm_action"], perm_lc, session["uid"])


# active user
@app.route('/<appname>/active/user', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def active_user(appname):
    required_list = ('id', 'is_active')
    data = check_required_params(request, required_list)
    if isinstance(data, Response):
        return data
    return user_active(appname, data)
