# -*- coding:utf-8 -*-
import logging


from armory.marine.util import now_timestamp
from resource_console.model.base import ModelBase
from resource_console import settings


_LOGGER = logging.getLogger("model")


class Icon(ModelBase):
    collection = 'icon'
    required = ('title', "icon", "platfrom")
    unique = ('title',)
    optional = (
        ("width", 0), ("height", 0),
        ("package", []), ("type", []),
        ("first_created", now_timestamp), ("last_modified", now_timestamp),
        ("refered_info", []))
    params = set(['platform', 'package', 'type', 'title', 'icon'])
    fields = {
        "platform": 1, "package": 1, "type": 1, "icon": 1, "title": 1}
    fields = {"first_created": 0, "refered_info": 0}

    @classmethod
    def new(cls, faq_dict):
        """
        creat icon instance
        """
        instance = cls()
        instance.title = faq_dict["title"]
        instance.icon = faq_dict["icon"]
        instance.guid = faq_dict["guid"]
        instance.download_url = faq_dict["download_url"]
        instance.platform = faq_dict["platform"]
        instance.width = faq_dict.get("width", 0)
        instance.height = faq_dict.get("height", 0)
        instance.package = faq_dict["package"]
        instance.type = faq_dict["type"]
        instance.refered_info = []
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)
