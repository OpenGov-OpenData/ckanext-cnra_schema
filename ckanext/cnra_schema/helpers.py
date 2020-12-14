import ckanext.cnra_schema.cnra_schema_utils as cnra_schema_utils

import logging

from ast import literal_eval

log = logging.getLogger(__name__)


def delete_existing_extra_from_package_dict(key, package_dict):
    existing_extra = {}
    extras_list = package_dict.get('extras', [])
    for extra in extras_list:
        if extra['key'] == key:
            existing_extra = extra

    if existing_extra:
        package_dict['extras'].remove(existing_extra)


def set_waf_map_fields(package_dict, iso_values, map_fields):
    if map_fields:
        for map_field in map_fields:
            source_field = map_field.get('source')
            target_field = map_field.get('target')
            default_value = map_field.get('default')
            value = iso_values.get(source_field, default_value)

            # If value is a list, convert to string
            if isinstance(value, list):
                value = ', '.join(str(x) for x in value)

            package_dict[target_field] = value

            # Remove from extras any keys present in the config
            delete_existing_extra_from_package_dict(target_field, package_dict)

    return package_dict


def set_waf_publisher_values(package_dict, iso_values, publisher_mapping):
    publisher_field = publisher_mapping.get('publisher_field')

    if publisher_field:
        publisher_name = iso_values.get('publisher') or \
                         publisher_mapping.get('default_publisher')
        package_dict[publisher_field] = publisher_name

        # Remove from extras any keys present in the config
        delete_existing_extra_from_package_dict(publisher_field, package_dict)

    return package_dict


def set_waf_contact_point(package_dict, iso_values, contact_point_mapping):
    name_field = contact_point_mapping.get('name_field')
    email_field = contact_point_mapping.get('email_field')

    if name_field:
        contact_point_name = iso_values.get('contact') or \
                           contact_point_mapping.get('default_name')
        package_dict[name_field] = contact_point_name

        # Remove from extras the name field
        delete_existing_extra_from_package_dict(name_field, package_dict)

    if email_field:
        contact_point_email = iso_values.get('contact-email') or \
                            contact_point_mapping.get('default_email')
        package_dict[email_field] = contact_point_email

        # Remove from extras the email field
        delete_existing_extra_from_package_dict(email_field, package_dict)

    return package_dict


def is_cnra_schema_field_populated(package_dict, field):
    field_name = field.get('field_name')

    if package_dict.get(field_name) and field_name not in 'spatial_details' \
            and field.get('preset') in ['composite', 'composite_repeating']:

        subfield_literal_eval = literal_eval(package_dict.get(field_name))

        return is_dict_populated(subfield_literal_eval)

    """"
    NOTE: This function returns True due to the front-end calling this helper function as an AND in the conditional.
    If this function returns False, the whole condition would be false and non-composite fields would not be included
    in the "Additional Metadata" table.
    """
    return True


def is_dict_populated(package_dict_field):
    is_subfield_empty = False

    if package_dict_field and isinstance(package_dict_field, dict):
        return is_sub_dict_populated_recursively_impl(package_dict_field, is_subfield_empty)
    elif isinstance(package_dict_field, list):
        is_subfield_list_populate = [is_sub_dict_populated_recursively_impl(x, is_subfield_empty)
                                     for x in package_dict_field]
        return True in is_subfield_list_populate
    else:
        return False


def is_sub_dict_populated_recursively_impl(pkg_dict_field_sub_dict, is_dict_empty):
    for v in pkg_dict_field_sub_dict.values():
        if isinstance(v, dict):
            is_dict_empty = is_sub_dict_populated_recursively_impl(v, is_dict_empty)
        elif v and isinstance(v, str):
            return True
        elif v and isinstance(v, list):
            converted_string = cnra_schema_utils.convert_list_to_string(v)
            if converted_string:
                return True

    return is_dict_empty
