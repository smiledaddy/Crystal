# -*- coding:utf-8 -*-
import logging
from werkzeug.wrappers import Response

from armory.marine.access_control import access_control, exception_handler
from rule_console.api import request, app
from rule_console.decorator import check_url_params, perf_logging
from rule_console.view.common import (
    create, info_list, info_get, info_mod, info_del, get_package_display_data)
from rule_console.utils.common import get_list_cond, get_valid_params
from rule_console.view.common_support import get_model_cls

_LOGGER = logging.getLogger(__name__)


API_LIST = '/<appname>/rule/v1/<modelName>/list'
API_ADD = '/<appname>/rule/v1/<modelName>/add'
API_EDIT = '/<appname>/rule/v1/<modelName>/edit'
API_DISPLAY = '/<appname>/rule/v1/package/getDisplayData'
API_UPDATE = '/<appname>/rule/v1/<modelName>/update'
API_DELETE = '/<appname>/rule/v1/<modelName>/delete'


@app.route(API_LIST, methods=['GET', ])
@perf_logging
@exception_handler
@access_control
@check_url_params
def list_info(appname, modelName):
    '''
        list api for show rule list.
        Request URL:  /<appname>/rule/v1/<modelname>/list
        Http Method:  GET
        Parameters : index, limit
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"海豚英文版",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"海豚英文版1",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    }
                ]
            }
        }
     '''
    MODELNAME = get_model_cls(modelName)
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    cond = get_list_cond(appname, request, MODELNAME)
    sort = [("_id", -1)]
    return info_list(appname, MODELNAME, cond, index, limit, sort)


@app.route(API_ADD, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def add_info(appname, modelName):
    '''
        create api to add rule.
        Request URL:  /appname/rule/rule/add
        Http Method: POST
        Parameters :
            {
                "title": "xxxx",
                "code::"xxxx", #operator need
                "package_name:"xxxx" #package need
            }
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"海豚英文版",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    }
                ]
            }
        }
    '''
    MODELNAME = get_model_cls(modelName)
    # check post data
    data = get_valid_params(request, MODELNAME.params)
    if isinstance(data, Response):
        return data
    # view logic
    return create(appname, MODELNAME, data)


@app.route(API_EDIT, methods=['GET', ])
@perf_logging
@exception_handler
@access_control
@check_url_params
def get_info(appname, modelName):
    '''
        this api is used to view one rule
        Request URL:  /<appname>/rule/<modelName>/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"海豚英文版"
            }
        }
     '''
    required_list = {
        'id&need&int',
    }
    data = get_valid_params(request, required_list)
    if isinstance(data, Response):
        return data
    # this method get info by id
    cond = {"_id": int(data["id"])}
    return info_get(appname, modelName, cond)


@app.route(API_DISPLAY, methods=['GET', ])
@perf_logging
@exception_handler
@access_control
@check_url_params
def package_get_display_data(appname):
    return get_package_display_data(appname)


@app.route(API_UPDATE, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def mod_info(appname, modelName):
    '''
        this api is used to modify one rule
        Request URL:  /appname/rule/rule/update
        HTTP Method:POST
        Parameters:
        {
           "id": 1,
           "title": "xxxx"
        }
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"海豚英文版"
            }
        }
    '''
    # check post data
    MODELNAME = get_model_cls(modelName)
    required_list = list(MODELNAME.params) + ["id&need&int", ]
    data = get_valid_params(request, required_list)
    if isinstance(data, Response):
        return data
    return info_mod(appname, MODELNAME, data)


@app.route(API_DELETE, methods=['POST', 'OPTIONS'])
@perf_logging
@exception_handler
@access_control
@check_url_params
def del_info(appname, modelName):
    '''
        this api is used to delete card from server,
        Request URL:  /appname/rule/rule/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete locale success",
                "data": {
                    "failed": [],
                    "success": [{"id": 3}, {"id":2}]
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
    return info_del(appname, modelName, data["items"])
