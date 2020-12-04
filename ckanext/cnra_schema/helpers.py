import json
import logging
import time

from dateutil.parser import parse
from six import text_type

log = logging.getLogger(__name__)


def delete_existing_extra_from_package_dict(key, package_dict):
    existing_extra = {}
    extras_list = package_dict.get('extras', [])
    for extra in extras_list:
        if extra['key'] == key:
            existing_extra = extra

    if existing_extra:
        package_dict['extras'].remove(existing_extra)


def get_date_and_time_dict(date_timestamp):
    if isinstance(date_timestamp, list) and len(date_timestamp) > 0:
        date_timestamp = date_timestamp[0]

    period = {
        'date': '',
        'time': ''
    }

    try:
        date_timestamp = parse(date_timestamp)
        period['date'] = date_timestamp.strftime("%Y-%m-%d")
        period['time'] = date_timestamp.strftime("%H:%M:%S")

    except ValueError:
        log.error('Error converting date and time string: {0}'.format(date_timestamp))

    period = json.dumps(period)
    return period


def convert_list_to_string(list_to_convert, delimiter=' '):
    if isinstance(list_to_convert, list):
        converted_str = delimiter.join(text_type(x) for x in list_to_convert)
        return converted_str

    return list_to_convert
