# -*- coding:utf-8 -*-
import logging
from werkzeug.wrappers import Response

from armory.marine.access_control import access_control, exception_handler
from rule_console.api import request, app
from rule_console.model.rule import Rule
from rule_console.view.rule import get_rule_display_data, delete_rule_info
from rule_console.decorator import check_url_params, perf_logging
from rule_console.utils.common import get_valid_params, check_rule_params
from rule_console.view.common import create, info_mod

_LOGGER = logging.getLogger(__name__)


API_GET_DISPLAYDATA = '/<appname>/rule/v1/rule/getDisplayData'
API_ADD_RULE = '/<appname>/rule/v1/rule/add'
API_UPDATE_RULE = '/<appname>/rule/v1/rule/update'
API_DELETE_RULE = '/<appname>/rule/v1/rule/delete'


@app.route(API_GET_DISPLAYDATA, methods=['GET', ])
@perf_logging
@exception_handler
@access_control
@check_url_params
def rule_get_display_data(appname):
    return get_rule_display_data(appname)


@app.route(API_ADD_RULE, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def rule_add(appname):
    '''
        create api to add rule.
        Request URL:  /appname/rule/rule/add
        Http Method: POST
        Parameters :
            {
                "title": "xxxx"
                "min_version": 0,
                "max_version": 0,
                "source":[1],
                "locale":[1],
                "operator":[1],
                "package":[1],
                "min_value": 0,
                "max_value": 0,
                "gray_scale": 100,
                "gray_start": 1
            }
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"海豚英文版",
                        "min_version": 0,
                        "max_version": 0,
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "min_version": 0,
                        "max_version": 0,
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    }
                ]
            }
        }

    '''
    # check post data
    data = get_valid_params(request, Rule.params)
    if isinstance(data, Response):
        return data

    # check the id of  pn/op/src/lc
    rule_params = ["package", "operator", "source", "locale"]
    data = check_rule_params(appname, data, rule_params)
    if isinstance(data, Response):
        return data

    # add logic
    return create(appname, Rule, data)


@app.route(API_UPDATE_RULE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def rule_update(appname):
    '''
        this api is used to modify one rule
        Request URL:  /appname/rule/rule/update
        HTTP Method:POST
        Parameters:
            {
                "title": "xxxx"
                "min_version": 0,
                "max_version": 0,
                "source":[1],
                "locale":[1],
                "operator":[1],
                "package":[1],
                "min_value": 0,
                "max_value": 0,
                "gray_scale": 100,
                "gray_start": 1
            }
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"海豚英文版",
                "min_version": 0,
                "max_version": 0,
                "first_created": "2015-02-05 21:37:38",
                "last_modified": "2015-02-05 21:37:38"
            }
        }
        '''
    # check post data
    required_list = list(Rule.params) + ["id&need&int", ]
    data = get_valid_params(request, required_list)
    if isinstance(data, Response):
        return data

    # check the id of  pn/op/src/lc
    rule_params = ["package", "operator", "source", "locale"]
    data = check_rule_params(appname, data, rule_params)
    if isinstance(data, Response):
        return data
    return info_mod(appname, Rule, data)


@app.route(API_DELETE_RULE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def rule_delete(appname):
    '''
        this api is used to delete rule,
        when one rule refered, the rule cannot removed
        Request URL:  /appname/rule/rule/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete rule success",
                "data": {
                    "failed": [],
                    "success": [{"id": 3}, {"id": 2}]
                }
    '''
    # check post data
    required_list = {
        'items&need&list',
    }
    data = get_valid_params(request, required_list)
    if isinstance(data, Response):
        return data

    # delete logic
    return delete_rule_info(appname, data["items"])
