# -*- coding:utf-8 -*-
import logging

from rule_console.model.package import Package
from rule_console.model.operator import Operator
from rule_console.model.source import Source
from rule_console.model.locale import Locale
from rule_console.model.rule import Rule

_LOGGER = logging.getLogger(__name__)
_MODELS = {
    Package.model_name: Package,
    Operator.model_name: Operator,
    Source.model_name: Source,
    Locale.model_name: Locale,
    Rule.model_name: Rule,
}


def get_model_cls(model_name):
    model_cls = _MODELS.get(model_name)
    return model_cls if model_cls else None
