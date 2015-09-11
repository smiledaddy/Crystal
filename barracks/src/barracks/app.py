# -*- coding:utf-8 -*-
"""
    barracks.app
    ~~~~~~~~~~~~~

    This model implements the central report application object.

"""
import logging
import sqlalchemy
import mongokit

from pylon.frame import App
from pylon.frame import Blueprint
from pylon.rest import manager
from pylon.rest.search import distinct_field
from pylon.rest.search import SearchParams
from pylon.rest.search import search
from pylon.rest.search import QueryBuilder
from pylon.rest.respcode import RespCode
from pylon.rest.helpers import inst_to_dict
from pylon.rest.helpers import dict_to_inst
from pylon.rest.helpers import update_relations
from pylon.rest.helpers import get_relations
from pylon.rest.helpers import strings_to_dates
from pylon.rest.helpers import has_field

_LOGGER = logging.getLogger('barracks')

DEFAULT_HTTP_HOST = '0.0.0.0'

DEFAULT_HTTP_PORT = 5000

DEFAULT_PROCESS_NUM = 4

ADMIN_METHODS = ['GET', 'POST', 'DELETE', 'PUT']


class Barracks(object):

    """Barracks application class.
    """
    BLUEPRINTNAME_FORMAT = '{0}{1}'

    URL_PREFIX = '/barracks'

    def __init__(self, app_name):
        self.app_name = app_name
        self.app = App(app_name)

    def init_conf(self, app_conf, model_list, debug=False):
        self.app_conf = app_conf
        self.postprocessors = app_conf.get('postprocessors', {})
        self.preprocessors = app_conf.get('preprocessors', {})
        for method in ('GET_MANY', ):
            self.postprocessors.setdefault(
                method, []).insert(0, self._add_filters)

        self.manager = manager.RESTManager(self.app)
        for model_class in model_list:
            postprocessors = getattr(model_class, 'postprocessors', {})
            preprocessors = getattr(model_class, 'preprocessors', {})
            # model level preprocessors will be applied after app level
            if isinstance(preprocessors, dict):
                for method, processors in self.preprocessors.iteritems():
                    preprocessors.setdefault(method, [])
                    preprocessors[method].extend(processors)
            # model level postprocessors will be applied before app level
            if isinstance(postprocessors, dict):
                for method, processors in self.postprocessors.iteritems():
                    postprocessors.setdefault(method, [])
                    postprocessors[method].extend(processors)
            # TODO: allow custom data validate and expose validation exception
            # to flask-restless, see http://goo.gl/4UajA8
            self.manager.create_api(
                model_class, methods=ADMIN_METHODS,
                allow_patch_many=app_conf.get('allow_patch_many', True),
                allow_delete_many=app_conf.get('allow_delete_many', True),
                preprocessors=preprocessors,
                postprocessors=postprocessors, url_prefix=Barracks.URL_PREFIX)
        self.DEBUG = debug

    def _add_filters(self, result=None, search_params=None, model=None):
        assert result['status'] == RespCode.OK
        filters_conf = getattr(model, '__filters__', {})

        multi_list = []
        cascade_dict = {}

        multi_conf_list = filters_conf.get('multi')
        cascade_conf_dict = filters_conf.get('cascade')

        if multi_conf_list is not None:
            # create multi filters list
            for filter_name in multi_conf_list:
                distinct_items = distinct_field(model, filter_name)
                multi_list.append({
                    'name': filter_name,
                    'items': sorted([
                        {
                            'value': v[0],
                            'display_value': v[0]
                        } for v in distinct_items],
                        key=lambda x: x['display_value'])
                })

        filters = {}
        if len(multi_list) > 0:
            filters.update({'multi': multi_list})
        if len(cascade_dict) > 0:
            filters.update({'cascade': cascade_dict})

        result['data']['filters'] = filters

    def run(self, host=DEFAULT_HTTP_HOST, port=DEFAULT_HTTP_PORT):
        self.app.run(host=host, port=port,
                     processes=DEFAULT_PROCESS_NUM,
                     debug=self.DEBUG)

    def _next_blueprint_name(self, basename):
        """Returns the next name for a blueprint with the specified base name.

        For example, if `basename` is ``'personapi'`` and blueprints already
        exist with names ``'personapi0'``, ``'personapi1'``, and
        ``'personapi2'``, then this function would return ``'personapi3'``.

        """
        # blueprints is a dict whose keys are the names of the blueprints
        blueprints = self.app.blueprints
        existing = [name for name in blueprints if name.startswith(basename)]
        # if this is the first one...
        if not existing:
            next_number = 0
        else:
            # for brevity
            b = basename
            existing_numbers = [int(n.partition(b)[-1]) for n in existing]
            next_number = max(existing_numbers) + 1
        return Barracks.BLUEPRINTNAME_FORMAT.format(basename, next_number)

    def create_api(self, api_path, methods, view_func):
        """This function used to add extend api for multalisk application
        `api_path`: the new api path without the part of api prefix
        `methods`: the http function supported by the new api, must be list
        `view_func`: the view function of the new api
        """
        # create new blueprint with different name from exists
        api_name = api_path.split('/')[-1]
        blueprintname = self._next_blueprint_name(api_name)
        blueprint = Blueprint(blueprintname,
                              self.app_name,
                              url_prefix=Barracks.URL_PREFIX)
        # add url rule to blueprint
        api_endpoint = (api_path if api_path.startswith('/') else
                        '/{0}'.format(api_path))
        api_methods = frozenset(methods)
        blueprint.add_url_rule(api_endpoint,
                               methods=api_methods,
                               view_func=view_func)
        self.app.register_blueprint(blueprint)

    def _search_data(self, model_class, search_filter):
        search_filter = SearchParams.inspect_filter(search_filter)
        if search_filter is None:
            msg = 'search_filter[%s] invalid!' % search_filter
            _LOGGER.warn(msg)
            raise Exception(msg)

        search_params = SearchParams.from_dictionary(search_filter)
        query = search(model_class, search_params)

        return query

    def get_data(self, model_class, search_filter):
        query = self._search_data(model_class, search_filter)
        db_type = getattr(model_class, '__db_type__', 'sqlorm')
        if db_type == 'sqlorm':
            objects = [inst_to_dict(model_class, x) for x in query]
        else:
            objects = [x for x in query]

        return objects

    def add_data(self, model_class, data_obj):
        """add new data to database, `data_obj` must be a json object
        """
        if type(data_obj) is not dict:
            raise Exception('data_obj is not dict!')

        session = getattr(model_class, '__session__')
        db_type = getattr(model_class, '__db_type__', 'sqlorm')

        if db_type == 'sqlorm':
            try:
                instance = dict_to_inst(model_class, data_obj)
                session.begin()
                session.add(instance)
                session.commit()
            except sqlalchemy.exc.SQLAlchemyError as e:
                _LOGGER.error("Save Data Error, %s", e)
        elif db_type == 'mongo':
            try:
                inst = session()
                inst.update(data_obj)
                inst.save()
            except mongokit.ValidationError as e:
                _LOGGER.error("Save Data Error, %s", e)
        else:
            pass

    def del_data(self, model_class, search_filter):
        session = getattr(model_class, '__session__')
        db_type = getattr(model_class, '__db_type__', 'sqlorm')
        if db_type == 'sqlorm':
            query = self._search_data(model_class, search_filter)
            try:
                session.begin()
                query.delete(synchronize_session=False)
                session.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                _LOGGER.warn('ORM IntergirtError:%s' % exception)
        elif db_type == 'mongo':
            try:
                filters = QueryBuilder.create_mongokit_filters(model_class,
                                                               search_filter)
                session.collection.remove(filters, safe=True)
            except Exception as e:
                _LOGGER.warn('delete error, %s', e)

    def mod_data(self, model_class, search_filter, data_obj):
        # validate data_obj
        if type(data_obj) is not dict:
            raise Exception('data_obj is not dict!')
        for field in data_obj:
            if not has_field(model_class, field):
                msg = "Model does not have field '{0}'".format(field)
                raise Exception(msg)

        session = getattr(model_class, '__session__')
        db_type = getattr(model_class, '__db_type__', 'sqlorm')

        # create query from query string
        query = self._search_data(model_class, search_filter)

        if db_type == 'sqlorm':
            relations = update_relations(model_class, query, data_obj)
            field_list = frozenset(data_obj) ^ relations
            data = dict((field, data_obj[field]) for field in field_list)

            # Special case: if there are any dates, convert the string form of
            # the date into an instance of the Python ``datetime`` object.
            data = strings_to_dates(model_class, data)

            try:
                # Let's update all instances present in the query
                num_modified = 0
                session.begin()
                if data:
                    for item in query.all():
                        for field, value in data.items():
                            setattr(item, field, value)
                        num_modified += 1
                session.commit()
            except Exception as exception:
                _LOGGER.exception(str(exception))
        elif db_type == 'mongo':
            try:
                filters = QueryBuilder.create_mongokit_filters(
                    model_class, search_filter)
                session.collection.update(filters, {'$set': data_obj},
                                          multi=True, safe=True)
            except Exception as exception:
                _LOGGER.exception(str(exception))
        else:
            pass
