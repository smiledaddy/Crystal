# -*- coding: utf-8 -*-
"""
    Simple demo for multalisk
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Http Request:
        http://x.x.x.x:5000/multalisk/report?app=1001&x_dimension=date&y_dimension=[{"name":"sum_uv","value":{"name":"uv","func":"sum"}}]&q={"filters":[{"name":"date","val":"2014-12-01","op":">="},{"name":"date","op":"<=","val":"2014-12-08"}]}

"""

import multalisk
from multalisk.model import orm
from multalisk.core.feature import ChartType


DEBUG = True
APP_CONF = {
    'model': [
        {"model_id": "1001", "db_conn": "mongodb://127.0.0.1/test?slaveOk=true"}
    ],
    'view': {
        'news001': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': '_id',
                    'y_dimension': [
                        {"name": "id_count", "value": {"func": "count"}},
                    ],
                    'default_q': {
                        "filters": [],
                        "order_by": [
                            {"field": "_id", "direction": "desc"}
                        ],
                        "limit": 3
                    },
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {
            }
        }
    }
}


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)


class User(object):
    __metaclass__ = app.MetaMongo
    __modelid__ = "1001"
    __collection__ = "user"


app.run(host='0.0.0.0')
