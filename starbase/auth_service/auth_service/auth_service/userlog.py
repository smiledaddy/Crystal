# coding = utf-8
import re
import time
import logging
import simplejson
from pymongo import MongoClient
from auth_service.settings import NAV_DICT, MONGO_CONFIG, USER_DBIP

from armory.tank.mongo import DESCENDING
from armory.marine.util import now_timestamp, unixto_string
from armory.marine.respcode import (
    OK, PERMISSION_DENY, UNKNOWN_ERROR, PARAM_ERROR)


_LOGGER = logging.getLogger(__name__)
_ONE_DAY = 86400.0
_MONGO_CONFIG = simplejson.loads(MONGO_CONFIG)
_DB = _MONGO_CONFIG.keys()[0]     # make sure at least one db config


def filter_url(url):
    '''
    as a comon url
     url: /pushadmin/modelname/list or
     /pushadmin/modlename/edit/2
    '''
    actions = ['online', 'add', 'update', 'delete', 'upload', 'offline']
    res_dict = {}
    if url:
        params = url.split('/')
        last_param = params[-1]
        if last_param in actions:
            res_dict = {
                'appname': params[-3],
                'modelname': params[-2],
                'action': last_param}
        else:
            res_dict = {
                'id': last_param,
                'action': params[-2],
                'modelname': params[-3],
                'appname': params[-4]}
    return res_dict


def get_userinfo(sid, db='usermanage'):
    # db = _DB
    client = MongoClient(host=USER_DBIP, port=27017)
    session_store = client[db]['sessions']
    user_store = client[db]['user']
    user_info = session_store.find_one({'sid': sid}, {'uid': 1})
    if user_info:
        uid = user_info.get('uid')
        user_name = user_store.find_one({'_id': uid}, {'user_name': 1})
        return user_name.get('user_name')
    else:
        return None


def save_userlog(save_dict, db='usermanage'):
    # db = _DB
    client = MongoClient(host=USER_DBIP, port=27017)
    userlog = client[db]['userlog']
    models = client[db]['modules']
    appname = save_dict.get('appname')
    save_dict.update({'appname': NAV_DICT[appname]})
    modelname = save_dict.get('modelname')
    m_info = models.find_one({'app_name': appname, 'module_name': modelname})
    save_dict.update({'modelname': m_info['module_value']})
    models = save_dict.pop('models', None)
    if models:
        for model in models:
            new_save_dict = save_dict.copy()
            max_art_id = userlog.find_one(
                {}, sort=[('_id', DESCENDING)], fields={'_id': 1})
            if max_art_id:
                new_save_dict.update({'_id': max_art_id['_id'] + 1})
            else:
                new_save_dict.update({'_id': 1})
            new_save_dict.update(model)
            userlog.insert(new_save_dict)


def save_loginfo(data_obj):
    act_info = {}
    sid = data_obj.get('sid')
    url = data_obj.get('url')
    rev_d = data_obj.get('data')
    try:
        src_d = simplejson.loads(simplejson.loads(rev_d))
        if src_d.get('data'):
            act_info.update({
                'msg': src_d.get('msg'),
                'status': src_d.get('status')})
            act_info = filter_url(url)
            if not act_info:
                return PARAM_ERROR
            # as the diff action, get diff data from respone data
            action = act_info.get('action')
            models = []
            if action in ['add', 'update']:
                model_dict = {
                    'modelid': src_d['data'].get('id'),
                    'modeltitle': src_d['data'].get('title') or
                    src_d['data'].get('name')}
                models.append(model_dict)
                act_info.update({'models': models})
            elif action in ['delete', 'online', 'offline', 'upload']:
                models = src_d['data'].get('userlog')
                memo = src_d['data'].get('memo')
                act_info.update({'models': models})
                act_info.update({'memo': memo})
            else:
                _LOGGER.error('action error, do not know this action')
                act_info.update({'models': None})
            user_name = get_userinfo(sid)
            if user_name:
                act_info.update({
                    'username': user_name,
                    'optime': now_timestamp()})
                save_userlog(act_info)
                return OK
            else:
                return PERMISSION_DENY
                _LOGGER.error('error no session, redirect login')
    except ValueError, e:
        _LOGGER.error(e)
        return UNKNOWN_ERROR


def search_cond(query={}):
    cond = {}
    start = end = 0
    start_time = query.get('start')
    end_time = query.get('end')
    if start_time and end_time:
        start = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
        end = time.mktime(time.strptime(end_time, '%Y-%m-%d')) + _ONE_DAY
        cond['optime'] = {'$gte': start, '$lte': end}
    searchKeyword = query.get('keyword')
    regex_cond_list = []
    if searchKeyword:
        try:
            modelid_cond = {}
            modelid_cond['modelid'] = int(searchKeyword)
            regex_cond_list.append(modelid_cond)
        except ValueError, e:
            _LOGGER.info(e)
        fields = ['appname', 'modelname', 'action', 'modeltitle', 'username']
        for field in fields:
            regex_cond = {}
            regex_cond[field] = {'$regex': re.escape(searchKeyword)}
            regex_cond_list.append(regex_cond)
        cond['$or'] = regex_cond_list
    return cond


def get_userlog(req_query={}, db='usermanage'):
    # db = _DB
    return_data = {}
    cond = search_cond(req_query)
    client = MongoClient(host=USER_DBIP, port=27017)
    userlog = client[db]['userlog']
    pageindex = req_query.get('index')
    pagesize = req_query.get('limit')
    sort_field = req_query.get('sort_field', '_id')
    sort_way = req_query.get('sort_way', -1)
    total = userlog.find(cond).count()
    raw_res = userlog.find(
        cond).sort(sort_field, sort_way).skip(
        pageindex * pagesize).limit(pagesize)
    log_list = []
    for res in raw_res:
        new_dict = {
            'id': res.get('_id'),
            'username': res.get('username'),
            'optime': unixto_string(res.get('optime')),
            'appname': res.get('appname'),
            'modelname': res.get('modelname'),
            'action': res.get('action'),
            'modelid': res.get('modelid'),
            'modeltitle': res.get('modeltitle'),
            'memo': res.get('memo')}
        log_list.append(new_dict)
    return_data['results'] = log_list
    return_data['total'] = total
    return return_data
