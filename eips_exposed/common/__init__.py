from typing import Any, Type
from datetime import datetime

from eips_exposed.common.config import CONFIG
from eips_exposed.common.exceptions import ConfigurationError, EIPParseError
from eips_exposed.common.logging import getLogger


def type_or_none(t: Type, v: Any) -> Any:
    try:
        v = t(v)
    except TypeError:
        return None
    else:
        return v


def int_or_none(v):
    return type_or_none(int, v)


def list_of_int_or_none(v):
    """ Process a list of ints or return None.

    Example:
    "1, 2, 3"
    """
    if not v:
        return None

    list_of_ints = []

    if ',' in v:
        vs = v.split(',')
        for each_v in vs:
            list_of_ints.append(int_or_none(each_v))
        return list_of_ints
    else:
        return [int_or_none(v)]


def datetime_or_none(v):
    """ Coerce a value to a datetime or None """
    if isinstance(v, datetime):
        return v
    try:
        v = datetime.strptime(v.strip(), '%Y-%m-%d')
    except ValueError:
        return None
    return v
