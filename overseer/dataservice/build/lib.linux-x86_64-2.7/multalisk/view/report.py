# -*- coding:utf-8 -*-
"""
    multalisk.view.report
    ~~~~~~~~~~~~~~~~~~~~~

    Provide report view for api layer by requests from client
"""
import json

from multalisk.model import MODEL_CONF
from multalisk.core.sql_helper import inst_to_dict
from multalisk.core.search import SearchParams
from multalisk.core.search import search
from multalisk.core.search import distinct_field
from multalisk.core.feature import create_feature
from multalisk.cache import (get_search_obj, set_search_obj,
                             get_filter_obj, set_filter_obj)
from multalisk.utils.exception import ParamError
from multalisk.utils.http_json import json_encode


def _get_model_info(model_id):
    """get model info by model_id from MODEL_CONF init at model/init.py
    """
    if model_id not in MODEL_CONF:
        msg = 'model id[%s] not configed in MODEL_CONF!' % model_id
        raise ParamError(msg)
    model_dict = MODEL_CONF[model_id]
    return (model_dict['db_type'],
            model_dict['model_class'],
            model_dict['mapped_db'])


def _cascade_filters(distinct_items, children, db_type, mapped_db,
                     model_class, filter_name):
    """Recuresive function, used for create cascade filters
    `children`: children node's conf dict or None
    `filter_name`: father node's field name
    """
    cascade_items = []
    for distinct_val in distinct_items:
        distinct_val = distinct_val[0]
        item_dict = {
            'display_value': distinct_val,
            'value': distinct_val
        }
        if children is not None and isinstance(children, dict):
            children_name = children['name']
            children_children = children.get('children')
            q = {
                "filters": [
                    {
                        "name": filter_name,
                        "op": "eq",
                        "val": distinct_val
                    }
                ]
            }
            c_distinct_items = distinct_field(db_type, mapped_db,
                                              model_class, children_name,
                                              search_params=q)
            children_items = _cascade_filters(c_distinct_items,
                                              children_children,
                                              db_type, mapped_db,
                                              model_class, children_name)
            item_dict.update({
                'children': {
                    'name': children_name,
                    'items': children_items
                }
            })
        cascade_items.append(item_dict)

    return cascade_items


def _create_filters(filters_conf):
    filters = {}
    cascade_dict = {}
    multi_list = []

    cascade_conf_dict = filters_conf.get('cascade')
    multi_conf_list = filters_conf.get('multi')

    if cascade_conf_dict is not None:
        # create cascade filters dict
        model_id = cascade_conf_dict['model_id']
        filter_name = cascade_conf_dict['name']
        children = cascade_conf_dict.get('children')

        db_type, model_class, mapped_db = _get_model_info(model_id)
        distinct_items = distinct_field(db_type, mapped_db,
                                        model_class, filter_name)
        cascade_items = _cascade_filters(distinct_items, children,
                                         db_type, mapped_db,
                                         model_class, filter_name)
        cascade_dict.update({
            'name': filter_name,
            'items': cascade_items
        })
    if multi_conf_list is not None:
        # create multi filters list
        for filter_item in multi_conf_list:
            model_id = filter_item['model_id']
            filter_name = filter_item['name']

            db_type, model_class, mapped_db = _get_model_info(model_id)
            distinct_items = distinct_field(db_type, mapped_db,
                                            model_class, filter_name)
            # check alias for filters just for ORM
            alias_dict = {}
            if db_type.endswith('sql'):
                col = getattr(model_class, filter_name)
                if hasattr(col, 'info') and col.info.get('alias'):
                    alias_dict = col.info['alias']

            multi_list.append({
                'name': filter_name,
                'items': sorted([
                    {
                        'value': v[0] if db_type.endswith('sql') else v,
                        'display_value': alias_dict.get(v[0]) or v[0]
                        if db_type.endswith('sql') else
                        alias_dict.get(v) or v
                    } for v in distinct_items],
                    key=lambda x: x['display_value'])
            })

    if len(multi_list) > 0:
        filters.update({'multi': multi_list})
    if len(cascade_dict) > 0:
        filters.update({'cascade': cascade_dict})

    return filters


def fetch_report(view_dict, search_filter):
    """Fetch report function, used for fetch final report for client
    by request, steps as follows.

        - step1: call search interface to get query objects by query string

        - step2: transform query object to python list by different db type

        - step3: create feature which defined in x_dimension and y_dimension
    """
    report_dict = {}
    chart_list = []

    charts_dict = view_dict['charts']
    filter_dict = view_dict['filters']
    # change it to always true if front-end not cache it
    enable_filter = True
    search_filter = SearchParams.inspect_filter(search_filter)
    # create charts data
    for chart_item in charts_dict:
        model_id = chart_item['model_id']
        x_dimension = chart_item['x_dimension']
        y_dimension = chart_item['y_dimension']
        order_by = chart_item.get('order_by')

        if search_filter:
            search_q = search_filter
            extend_q = chart_item.get('extend_q')
            if extend_q:
                if extend_q.get('filters') and search_q.get('filters'):
                    search_q['filters'].extend(extend_q['filters'])
                if extend_q.get('limit'):
                    search_q['limit'] = extend_q['limit']
                if extend_q.get('order_by'):
                    search_q['order_by'] = extend_q['order_by']
        else:
            search_q = chart_item['default_q']
        chart_type = chart_item['chart_type']

        db_type, model_class, mapped_db = _get_model_info(model_id)
        search_params = SearchParams.from_dictionary(search_q)
        search_obj = get_search_obj(db_type, model_class, search_params)
        if not search_obj:
            query = search(db_type, model_class, search_params)
            if db_type.endswith('sql'):
                objects = [inst_to_dict(model_class, x) for x in query]
            else:
                objects = [x for x in query]
            # save to cache
            search_obj = json_encode(objects)
            set_search_obj(db_type, model_class, search_params, search_obj)

        objects = json.loads(search_obj)
        feature_list = create_feature(chart_type,
                                      x_dimension, y_dimension,
                                      order_by, objects)
        chart_list.append(feature_list)

    report_dict.update({'items': chart_list})
    if enable_filter:
        filter_obj = get_filter_obj(filter_dict)
        if not filter_obj:
            filter_obj = _create_filters(filter_dict)
            # save to cache
            set_filter_obj(filter_dict, filter_obj)

        report_dict.update({'filters': filter_obj})

    return report_dict
