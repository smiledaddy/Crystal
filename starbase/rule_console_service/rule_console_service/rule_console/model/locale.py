# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Locale(ModelBase):
    model_name = "locale"
    collection = 'locale'
    required = ('title', )
    unique = ('title',)
    optional = (
        ('first_created', now_timestamp),
        ('last_modified', now_timestamp)
    )
    params = {
        'title&need&str',
    }
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"}
    }
    fields = {"title": 1}

    @classmethod
    def new(cls, data):
        """
        creat locale instance
        """
        instance = cls()
        instance.title = data["title"]
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)
