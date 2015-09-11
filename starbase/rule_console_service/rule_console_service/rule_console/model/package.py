# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Package(ModelBase):
    model_name = 'package'
    collection = 'package'
    required = ('title', 'package_name', )
    unique = ('title',)
    optional = (
        ("first_created", now_timestamp), ("last_modified", now_timestamp))
    params = {
        'platform&need&int',
        'title&need&str',
        'package_name&need&str'
    }
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"},
        "package_name": {"data_type": "string"}
    }
    fields = {"platform": 1, "title": 1, "package_name": 1}

    @classmethod
    def new(cls, data):
        """
        creat package instance
        """
        instance = cls()
        instance.title = data["title"]
        instance.platform = data["platform"]
        instance.package_name = data["package_name"]
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)
