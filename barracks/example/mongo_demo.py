#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tryao
# @Date:   2015-04-07 11:29:00
# @Last Modified by:   tryao
# @Last Modified time: 2015-04-10 14:40:27
from datetime import datetime
from time import mktime

from pylon.frame import App
from armory.tank.mongo_orm import Document, DocumentMeta, Connection

from barracks.app import Barracks

APP_CONF = {
    'DEBUG': True,
}

app = App(__name__)
app.config.update(APP_CONF)
conn = Connection(host='127.0.0.1', port=27017, database='admin')


def unix_time(value=None):
    if not value:
        value = datetime.utcnow()
    try:
        return int(mktime(value.timetuple()))
    except AttributeError:
        return 0


class Feedback(Document):
    __metaclass__ = DocumentMeta
    __tablename__ = 'feedback'
    __session__ = conn
    structure = {
        '_id': int,
        'type': int,
        'newsId': basestring,
        'content': unicode,
        'relatedIds': basestring,
        'locale': basestring,
        'phoneType': unicode,
        'status': int,
        'systemVersion': basestring,
        'browserVersion': basestring,
        'phonePixels': basestring,
        'createTime': int,
    }
    required_fields = [
        'type', 'newsId', 'relatedIds', 'locale',
        'phonePixels'
    ]
    default_values = {
        'status': 0,
        'content': u'',
        'createTime': unix_time,
        'phoneType': u'',
        'systemVersion': '',
        'browserVersion': '',
    }

    def validate(self, *args, **kwargs):
        if self['type'] == 0 and not self.get('content'):
            raise ValueError('content should not be empty when type==0')
        super(Feedback, self).validate(*args, **kwargs)

if __name__ == '__main__':
    model_list = [Feedback, ]
    app_conf = {}
    barracks_app = Barracks('demo')
    barracks_app.init_conf(app_conf, model_list, debug=True)
    # barracks_app.add_data(Feedback, {
    #     '_id': 1,  'type': 2, 'newsId': 'FAKE',
    #     'relatedIds': '', 'locale': 'zh-cnj', 'phonePixels': '1280,800'})
    # print barracks_app.get_data(
    #     Feedback, {'filters': [{'name': '_id', 'op': '==', 'val': 1}]})
    # barracks_app.mod_data(Feedback, {
    #     'filters': [{'name': '_id', 'op': '==', 'val': 1}]},
    #     {'systemVersion': 'android5.1'})
    # print barracks_app.get_data(
    #     Feedback, {'filters': [{'name': '_id', 'op': '==', 'val': 1}]})
    # barracks_app.del_data(Feedback, {'filters': [
    #     {'name': '_id', 'op': '==', 'val': 1}]})
    barracks_app.run()
