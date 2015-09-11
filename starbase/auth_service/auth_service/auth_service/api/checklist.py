# -*- coding:utf-8 -*-
import logging


from armory.marine.access_control import access_control, exception_handler
from armory.marine.respcode import AUTH_ERROR
from armory.marine.json_rsp import json_response_error
from auth_service.api import request, session, app
from auth_service.decorator import check_url_params
from auth_service.utils.common import check_required_params
from auth_service.view.checklist import check_content, checklist_create

_LOGGER = logging.getLogger('auth_service')


@app.route(
    '/<projectname>/<appname>/<applabel>/<module>/check/<id>',
    methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def check_info(appname, projectname, applabel, module, id):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    uid = session.get('uid')
    required_list = ("checked", "mark")
    data = check_required_params(request, required_list)
    data["uid"] = uid
    return check_content(appname, projectname, applabel, module, id, data)


@app.route(
    '/<projectname>/<appname>/<applabel>/<module>/submit',
    methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
@check_url_params
def submit_info(projectname, appname, applabel, module):
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    uid = session.get('uid')
    required_list = ("items", )
    data = check_required_params(request, required_list)
    # view logic
    return checklist_create(
        appname, projectname, applabel, module, uid, data["items"])
