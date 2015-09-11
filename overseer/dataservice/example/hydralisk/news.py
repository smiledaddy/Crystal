import os
import logging.config
from datetime import date, timedelta

from redis import StrictRedis

from hydralisk.app import Hydralisk
from multalisk.core.feature import ChartType
from multalisk.model import orm
from multalisk.utils.custom_filter import n_days_ago
from multalisk.model.base import MetaSQL


DEBUG = True
LOG_FILE = '/tmp/hydralisk.log'
LOG_ERR_FILE = '/tmp/hydralisk.err'
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
REDIS_CONN = StrictRedis(host='127.0.0.1', port=6379, db=7)


LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(process)d %(levelname)s %(asctime)s %(message)s'
        },
        'detail': {
            'format': '%(process)d %(levelname)s %(asctime)s '
            '[%(module)s.%(funcName)s line:%(lineno)d] %(message)s',
        },
    },
    'handlers': {
        'overseer': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILE,
        },
        'err_file': {
            'level': 'WARN',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_ERR_FILE,
        },
    },
    'loggers': {
        'demo': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'multalisk': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'hydralisk': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'armory': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)

_LOGGER = logging.getLogger('demo')

TOTAL_EMAIL_COUNT = 4


def is_dump_done():
    dump_key = 'news_dump_%s' % (date.today() - timedelta(days=1))
    dump_flag = REDIS_CONN.get(dump_key)
    if dump_flag is not None and int(dump_flag) < TOTAL_EMAIL_COUNT:
        done_count = int(REDIS_CONN.incr(dump_key))
        if done_count == TOTAL_EMAIL_COUNT:
            _LOGGER.info('all mail sent, delete flag...')
            REDIS_CONN.delete(dump_key)
        return True
    else:
        return False

APP_CONF = {
    'model': [
        {"model_id": "1001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1101", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1102", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1103", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1104", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1105", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1106", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2101", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2102", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2103", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2104", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2105", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2106", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3101", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3102", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3103", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3104", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3105", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3106", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4101", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4102", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4103", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4104", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4105", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4106", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
    ],
    'view': {
        'click_top100': {
            'charts': [{
                'model_id': '1006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        'field': 'source',
                        'func': 'no_func',
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '2006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '3006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '4006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }],
            'schedule': ('*/15 2-6 * * *', is_dump_done, None),
            'template': os.path.join(CUR_DIR, 'click_top100.html'),
        },
        'app_click_top100': {
            'charts': [{
                'model_id': '1106',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        'field': 'source',
                        'func': 'no_func',
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '2106',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '3106',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '4106',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "source",
                    "value": {
                        "field": "source",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }, {
                    "name": "top_click",
                    "value": {
                        "field": "top_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "home_click",
                    "value": {
                        "field": "home_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "push_click",
                    "value": {
                        "field": "push_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }],
            'schedule': ('*/15 2-6 * * *', is_dump_done, None),
            'template': os.path.join(CUR_DIR, 'app_click_top100.html'),
        },
        'category_click_rate': {
            'charts': [{
                'model_id': '1003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '2003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '3003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '4003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }],
            'schedule': ('*/15 2-6 * * *', is_dump_done, None),
            'template': os.path.join(CUR_DIR,
                                     'category_click_rate.html'),
        },
        'app_category_click_rate': {
            'charts': [{
                'model_id': '1103',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '2103',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '3103',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '4103',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }],
            'schedule': ('*/15 2-6 * * *', is_dump_done, None),
            'template': os.path.join(CUR_DIR,
                                     'app_category_click_rate.html'),
        },
    },

    'mail': {
        'server': 'smtp.gmail.com:587',
        'user': 'backend.service.alert',
        'passwd': 'backend.P@55word',
        'from': 'Dolphin Service Statistics<backend.service.alert@gmail.com>',
        'to': ['xshu@bainainfo.com', 'tryao@bainainfo.com',
               'xyren@bainainfo.com', 'zhxhe@bainainfo.com',
               'shjmi@bainainfo.com', 'nlu@bainainfo.com',
               'qlu@bainainfo.com', 'rli@bainainfo.com',
               'snma@bainainfo.com', 'jjjiang@bainainfo.com'] if not DEBUG else [
            'tryao@bainainfo.com']
    },
    'render': {
        'server': 'http://127.0.0.1:3005',
        'upload': False,
    }
}


app = Hydralisk('test')
app.init_conf(APP_CONF)

_CATEGORY_MAP = {
    1: "Important News",
    2: "International",
    3: "National",
    4: "Society",
    5: "Entertainment",
    6: "Sport",
    7: "Finance",
    8: "Technology",
    9: "Military",
    10: "Auto",
    11: "History",
    12: "Other",
    13: "Life",
    14: "Education",
    15: "Humor",
    16: "Smart Phone",
    17: "Magazine",
    18: "Politics",
    19: "Art & Culture",
    20: "Fashion",
    21: "Religion",
    22: "Taiwan",
    23: "Stock",
    24: "Law",
    25: "Environment",
    26: "Travel",
    27: "Beauty",
    29: "Ramadan",
    30: "Accident",
    31: "Abdomen",
    32: "Provinces",
    33: "Science",
    34: "Capital",
    35: "Health",
    36: "Royal Family",
    37: "Cross-Strait",
    38: "Views",
    40: "Woman",
    41: "Famous & Star",
    42: "Game",
    43: "TV Series",
    44: "House",
    46: "Food",
    47: "Moment",
    48: "Man",
    51: "Russia",
    52: "World",
    53: "Popular",
    54: "India",
    55: "Quiz",
    56: "Cricket"
}
_PRIORITY_MAP = {
    8: "P0",
    0: "P1",
    4: "P2",
    -1: "Publish To Tab",
    -16: "UnPublished",
    - 20: "Auto",
    -100: "Uncategorized",
}


class News_report_origin_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_origin_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2001"
    __tablename__ = "report_origin_ru_ru"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3001"
    __tablename__ = "report_origin_ja_jp"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4001"
    __tablename__ = "report_origin_ar_sa"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1101"
    __tablename__ = "report_origin_tr_tr_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2101"
    __tablename__ = "report_origin_ru_ru_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3101"
    __tablename__ = "report_origin_ja_jp_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4101"
    __tablename__ = "report_origin_ar_sa_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1002"
    __tablename__ = "report_type_sum_tr_tr"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2002"
    __tablename__ = "report_type_sum_ru_ru"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3002"
    __tablename__ = "report_type_sum_ja_jp"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4002"
    __tablename__ = "report_type_sum_ar_sa"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1102"
    __tablename__ = "report_type_sum_tr_tr_app"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2102"
    __tablename__ = "report_type_sum_ru_ru_app"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3102"
    __tablename__ = "report_type_sum_ja_jp_app"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4102"
    __tablename__ = "report_type_sum_ar_sa_app"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1003"
    __tablename__ = "report_category_sum_tr_tr"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2003"
    __tablename__ = "report_category_sum_ru_ru"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3003"
    __tablename__ = "report_category_sum_ja_jp"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4003"
    __tablename__ = "report_category_sum_ar_sa"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1103"
    __tablename__ = "report_category_sum_tr_tr_app"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2103"
    __tablename__ = "report_category_sum_ru_ru_app"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3103"
    __tablename__ = "report_category_sum_ja_jp_app"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4103"
    __tablename__ = "report_category_sum_ar_sa_app"
    category = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1004"
    __tablename__ = "report_priority_sum_tr_tr"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2004"
    __tablename__ = "report_priority_sum_ru_ru"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3004"
    __tablename__ = "report_priority_sum_ja_jp"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4004"
    __tablename__ = "report_priority_sum_ar_sa"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1104"
    __tablename__ = "report_priority_sum_tr_tr_app"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2104"
    __tablename__ = "report_priority_sum_ru_ru_app"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3104"
    __tablename__ = "report_priority_sum_ja_jp_app"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4104"
    __tablename__ = "report_priority_sum_ar_sa_app"
    priority = orm.Column(
        orm.Integer, primary_key=True, info={'alias': _PRIORITY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1005"
    __tablename__ = "report_source_sum_tr_tr"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2005"
    __tablename__ = "report_source_sum_ru_ru"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3005"
    __tablename__ = "report_source_sum_ja_jp"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4005"
    __tablename__ = "report_source_sum_ar_sa"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1105"
    __tablename__ = "report_source_sum_tr_tr_app"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2105"
    __tablename__ = "report_source_sum_ru_ru_app"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3105"
    __tablename__ = "report_source_sum_ja_jp_app"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4105"
    __tablename__ = "report_source_sum_ar_sa_app"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_tr_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1006"
    __tablename__ = "report_news_sum_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ru_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2006"
    __tablename__ = "report_news_sum_ru_ru"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ja_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3006"
    __tablename__ = "report_news_sum_ja_jp"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ar_sa(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4006"
    __tablename__ = "report_news_sum_ar_sa"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_tr_tr_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1106"
    __tablename__ = "report_news_sum_tr_tr_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ru_ru_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2106"
    __tablename__ = "report_news_sum_ru_ru_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ja_jp_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3106"
    __tablename__ = "report_news_sum_ja_jp_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ar_sa_app(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4106"
    __tablename__ = "report_news_sum_ar_sa_app"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer, info={'alias': _CATEGORY_MAP})
    priority = orm.Column(orm.Integer, info={'alias': _PRIORITY_MAP})
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)

app.run(worker_num=1)
