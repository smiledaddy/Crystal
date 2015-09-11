# -*- coding: utf-8 -*-
import logging


from armory.marine.util import now_timestamp
from base import ModelBase

_LOGGER = logging.getLogger("model")


class CheckList(ModelBase):
    collection = 'checklist'
    required = ('projectname', 'appname', 'modulename', 'status', 'mark')
    unique = ()
    optional = (
        ('first_created', now_timestamp),
        ('last_modified', now_timestamp)
    )
    params = set(['app_name', 'module_name', 'check_id'])

    @classmethod
    def new(
            cls, projectname, app_name, module_name, id,
            uid, check_uid=[], status=1, mark=''):
        '''
        create app instance
        '''
        instance = cls()
        instance.data = {}

        instance.data['projectname'] = projectname
        instance.data['app_name'] = app_name
        instance.data['module_name'] = module_name
        instance.data['check_id'] = id
        instance.data['submit_uid'] = uid
        instance.data['check_uid'] = check_uid
        instance.data['mark'] = mark
        instance.data['status'] = status
        instance.data['first_created'] = now_timestamp()
        instance.data['last_modified'] = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data['_id'] = max_id
        return cls.insert(appname, instance.data)
