# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")
_MAX_VERSION = 4294967295


class Rule(ModelBase):
    model_name = "rule"
    collection = 'rule'
    required = ('platform', 'title', 'package', 'operator', 'source', 'locale')
    unique = ('title', )
    optional = (
        ('first_created', now_timestamp), ('last_modified', now_timestamp))
    params = set(['title', ])
    params = {
        'platform&need&int',
        'title&need&str',
        'package&need&list',
        'operator&option&list',
        'source&option&list',
        'locale&option&list',
        'min_version&need&int',
        'max_version&option&int&4294967295',
        'min_value&option&int&0',
        'max_value&option&int&0',
        'gray_start&option&int&1',
        'gray_scale&option&int&100',
    }
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"},
        "min_version": {"data_type": "int"},
        "max_version": {"data_type": "int"}
    }
    fields = {
        "first_created": 0, "last_modified": 0}

    @classmethod
    def new(cls, rule_dict):
        """
        creat source instance
        """
        instance = cls()
        instance.title = rule_dict["title"]
        instance.platform = rule_dict["platform"]
        instance.package = rule_dict["package"]
        instance.operator = rule_dict["operator"]
        instance.source = rule_dict["source"]
        instance.locale = rule_dict["locale"]
        instance.min_version = rule_dict["min_version"]
        instance.max_version = rule_dict.get("max_version", _MAX_VERSION)
        instance.min_value = rule_dict.get("min_value", 0)
        instance.min_value = rule_dict.get("min_value", 0)
        instance.max_value = rule_dict.get("max_value", 0)
        instance.gray_start = rule_dict.get("gray_start", 1)
        instance.gray_scale = rule_dict.get("gray_scale", 100)
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance["_id"] = max_id
        return cls.insert(appname, instance)
