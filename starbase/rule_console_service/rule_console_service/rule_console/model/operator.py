# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Operator(ModelBase):
    model_name = "operator"
    collection = 'operator'
    required = ('title', "code")
    unique = ('title',)
    optional = (
        ('first_created', now_timestamp),
        ('last_modified', now_timestamp)
    )
    params = {
        'title&need&str',
        'code&need&str'
    }
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"}
    }
    fields = {"title": 1, "code": 1}

    @classmethod
    def new(cls, data):
        """
        creat operator instance
        """
        instance = cls()
        instance.title = data["title"]
        instance.code = data["code"]
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)
