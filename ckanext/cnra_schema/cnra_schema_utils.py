import json
import logging
import unicodecsv as csv
from dateutil.parser import parse
from six import text_type

import ckan.model as model
from ckan.common import config
from ckan.plugins.toolkit import (
    ObjectNotFound,
    NotAuthorized,
    get_action,
    abort,
    c,
    _
)
from ckanext.scheming import helpers

log = logging.getLogger(__name__)


def delete_existing_extra_from_package_dict(key, package_dict):
    existing_extra = {}
    extras_list = package_dict.get('extras', [])
    for extra in extras_list:
        if extra['key'] == key:
            existing_extra = extra

    if existing_extra:
        extras_list.remove(existing_extra)


def get_date_and_time_dict(date_timestamp):
    original_date_timestamp_string = ''
    if isinstance(date_timestamp, list) and len(date_timestamp) > 0:
        original_date_timestamp_string = date_timestamp[0]

    period = {
        'date': '',
        'time': ''
    }

    try:
        if original_date_timestamp_string:
            date_timestamp_parsed = parse(original_date_timestamp_string)
            date = ''
            time = ''

            if date_timestamp_parsed.year < 1900:
                date_timestamp_tokens = original_date_timestamp_string.strip().split("T")
                date = date_timestamp_tokens[0]

                if len(date_timestamp_tokens) > 1:
                    time_tokens = date_timestamp_tokens[1].strip().split("Z")
                    time = time_tokens[0]
            else:
                date = date_timestamp_parsed.strftime('%Y-%m-%d')
                time = date_timestamp_parsed.strftime('%H:%M:%S')

            period['date'] = date

            if ':' in original_date_timestamp_string:
                period['time'] = time

    finally:
        period = json.dumps(period)

    return period


def convert_list_to_string(list_to_convert, delimiter=' '):
    if isinstance(list_to_convert, list):
        converted_str = delimiter.join(text_type(x) for x in list_to_convert)
        return converted_str

    return list_to_convert


def get_package_groups(groups_dict):
    """
    Build out the group names comma separated string
    """
    groups = [group.get('display_name') for group in groups_dict]
    return ",".join(groups)


def get_package_tags(tags_dict):
    """
    Build out the tag names comma separated string
    """
    tags = [tag.get('display_name') for tag in tags_dict]
    return ",".join(tags)


def metadata_download(package_id, response):
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user
    }

    data_dict = {
        'id': package_id
    }
    try:
        result = get_action('package_show')(context, data_dict)
    except (ObjectNotFound, NotAuthorized):
        abort(404, _('Package not found'))

    dataset_fields = helpers.scheming_get_dataset_schema("dataset")['dataset_fields']

    if hasattr(response, u'headers'):
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = \
            'attachment; filename="{name}-metadata.csv"'.format(name=package_id)

    wr = csv.writer(response.stream, encoding='utf-8')

    header = ['Field', 'Value']
    wr.writerow(header)

    for field in dataset_fields:
        if field['field_name'] == 'tag_string':
            value = get_package_tags(result.get('tags'))
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                value
            ])
        elif field['field_name'] == 'owner_org':
            org_alias = str(config.get('ckan.organization_alias', 'Organization'))
            wr.writerow([
                org_alias,
                result['organization']['title']
            ])
        elif field['field_name'] in ['group', 'groups']:
            group_alias = str(config.get('ckan.group_alias', 'Group'))+'s'
            value = get_package_groups(result.get('groups'))
            wr.writerow([
                group_alias,
                value
            ])
        elif helpers.scheming_field_choices(field):
            value = helpers.scheming_choices_label(
                helpers.scheming_field_choices(field),
                result.get(field['field_name'])
            )
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                value
            ])
        else:
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                result.get(field['field_name'])
            ])

    return response