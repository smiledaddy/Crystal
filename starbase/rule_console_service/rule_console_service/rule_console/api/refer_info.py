# -*- coding:utf-8 -*-
import logging
from werkzeug.wrappers import Response

from armory.marine.access_control import access_control, exception_handler
from armory.marine.json_rsp import json_response_ok
from rule_console.api import request, app
from rule_console.view.refered_info import (
    add_refered_info, delete_refered_info)
from rule_console.decorator import check_url_params, perf_logging
from rule_console.model.refered_info import ReferInfo
from rule_console.utils.common import get_valid_params


_LOGGER = logging.getLogger(__name__)


API_ADD_REFER = '/<appname>/rule/v1/referInfo/add'
API_DELETE_REFER = '/<appname>/rule/v1/referInfo/delete'


@app.route(API_ADD_REFER, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def refer_info_add(appname):
    '''
        create api to add refered info.
        Request URL:  /appname/rule/referInfo/add
        Http Method: POST
        Parameters :
        {
           "target_field": "rule",
           "target_id": 1,
           "refered_data":{
                "modelName" : "category",
                "id" : 1,
                "modelField" : "rule"
            }
        }
        Return :
        {
            "status":0
            "data":{}
        }

    '''
    # check post data
    data = get_valid_params(request, ReferInfo.params)
    if isinstance(data, Response):
        return data

    # get required args
    target_field = data.get("target_field")
    target_id = int(data.get("target_id"))
    refered_data = data.get("refered_data")
    old_id = data.get("old_target_id")

    # add logic
    add_refered_info(
        appname, target_field, target_id, refered_data, old_id)

    return json_response_ok({}, msg="add refered info  success")


@app.route(API_DELETE_REFER, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def refer_info_delete(appname):
    '''
        this api is used to de refered info,
        Request URL:  /appname/rule/referInfo/delete
        HTTP Method: POST
        Parameters:
        {
           "target_field": "rule",
           "target_id": 1,
           "unrefered_data":{
                "modelName" : "category",
                "id" : 1,
                "modelField" : "rule"
            }
        }
        Return:
            {
                "status": 0,
                "msg": "de refered info success",
                "data": {}
    '''
    # check post data
    params = {
        'target_field&need&str',
        'target_id&need&int',
        "unrefered_data&need&dict",
    }
    data = get_valid_params(request, params)
    if isinstance(data, Response):
        return data
    target_field = data.get("target_field")
    target_id = int(data.get("target_id"))
    unrefered_data = data.get("unrefered_data")

    delete_refered_info(appname, target_field, target_id, unrefered_data)
    return json_response_ok({})
