#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tryao
# @Date:   2015-04-07 11:29:00
# @Last Modified by:   tryao
# @Last Modified time: 2015-04-10 11:52:30
from datetime import datetime
from time import mktime

from pylon.frame import App
from armory.tank.mongo_orm import Document, DocumentMeta, Connection, ObjectId

from barracks.app import Barracks

APP_CONF = {
    'DEBUG': True,
}

app = App(__name__)
app.config.update(APP_CONF)
conn = Connection(host='127.0.0.1', port=27017, database='overseer')


def unix_time(value=None):
    if not value:
        value = datetime.utcnow()
    try:
        return int(mktime(value.timetuple()))
    except AttributeError:
        return 0


class Report(Document):
    __metaclass__ = DocumentMeta
    __tablename__ = 'report'
    __session__ = conn
    structure = {
        '_id': ObjectId,
        'date': unicode,
        'network': unicode,
        'location': unicode,
        'version': unicode,
        'action': unicode,
        'label': unicode,
        'uv': int,
        'click': int,
    }
    required_fields = [
        'date', 'location', 'version', 'uv', 'click'
    ]
    default_values = {
        'network': u'TYPE_00',
        'action': u'action_00',
        'label': u'label_00',
    }

    #def validate(self, *args, **kwargs):
    #    if self['type'] == 0 and not self.get('content'):
    #        raise ValueError('content should not be empty when type==0')
    #    super(Feedback, self).validate(*args, **kwargs)

if __name__ == '__main__':
    model_list = [Report, ]
    app_conf = {}
    barracks_app = Barracks('test')
    barracks_app.init_conf(app_conf, model_list, debug=True)
    # barracks_app.add_data(Feedback, {
    #     '_id': 1,  'type': 2, 'newsId': 'FAKE',
    #     'relatedIds': '', 'locale': 'zh-cnj', 'phonePixels': '1280,800'})
    # print barracks_app.get_data(
    #     Feedback, {'filters': [{'name': '_id', 'op': '==', 'val': 1}]})
    # barracks_app.del_data(Feedback, {'filters': [
    #     {'name': '_id', 'op': '==', 'val': 1}]})
    barracks_app.run(port=5002)
