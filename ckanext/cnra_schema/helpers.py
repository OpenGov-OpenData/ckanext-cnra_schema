import json
import logging
import time

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
    date_timestamp = convert_list_to_string(date_timestamp)

    period = {
        'date': '',
        'time': ''
    }

    date_timestamp_len = len(date_timestamp)
    if date_timestamp_len > 10:
        try:
            time.strptime(date_timestamp, "%Y-%m-%dT%H:%M:%SZ")
            period['date'] = date_timestamp[:10]
            period['time'] = date_timestamp[11:date_timestamp_len - 1]

        except ValueError:
            log.error('Error converting date and time string: {0}'.format(date_timestamp))

    elif date_timestamp_len == 10:
        try:
            time.strptime(date_timestamp, "%Y-%m-%d")
            period['date'] = date_timestamp

        except ValueError:
            log.error('Error converting date string: {0}'.format(date_timestamp))

    period = json.dumps(period)
    return period


def convert_list_to_string(list_to_convert, delimiter=' '):
    if isinstance(list_to_convert, list):
        converted_str = delimiter.join(text_type(x) for x in list_to_convert)
        return converted_str

    return list_to_convert
