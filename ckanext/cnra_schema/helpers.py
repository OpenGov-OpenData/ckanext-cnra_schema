import ckanext.cnra_schema.cnra_schema_utils as cnra_schema_utils
from ast import literal_eval

import logging

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


def composite_repeating_get_formatted_contact_address_dict(package_dict_field):
    address_line1 = package_dict_field['address']
    address_line2 = ''

    address_line2 = '{0}, {1} {2} {3}'.format(package_dict_field['city'], package_dict_field['state'],
                                              package_dict_field['postalCode'], package_dict_field['country'])

    address_dict = {
        'addressLine1': address_line1,
        'addressLine2': address_line2,
    }

    return address_dict


def is_composite_field_populated(package_dict, field):
    """"
    This function checks if a composite field populated. Non-composite fields will return True by default.
    """
    field_name = field.get('field_name')

    if package_dict.get(field_name) and field_name not in 'spatial_details' \
            and field.get('preset') in ['composite', 'composite_repeating', 'contact_address_composite_repeating',
                                        'cnra_composite_repeating', 'geologic_age_composite']:

        subfield_literal_eval = {}
        try:
            subfield_literal_eval = literal_eval(package_dict[field_name])
        except (ValueError, SyntaxError) as e:
            log.debug('Unable to evaluate field {0} in package dictionary: {1}'
                      .format(field_name, package_dict.get(field_name)))

        return is_dict_populated(subfield_literal_eval)

    return True


def is_dict_populated(package_dict_field):
    """
    Recursively checks if package dictionary field is populated. Since the field is a composite field, it will be nested
    with either a dictionary or list.
    :param package_dict_field:
    :return: Boolean value depending on if the composite field is populated
    """
    primitive_types = (str, int, float, complex, bool, bytes)
    is_dict_populated_bool = False
    if isinstance(package_dict_field, dict):
        for val in package_dict_field.values():
            if val and isinstance(val, dict):
                is_dict_populated_bool = is_dict_populated(val)
            elif val and isinstance(val, list):
                is_dict_populated_bool = any((is_dict_populated(x) for x in val))
            elif val and isinstance(val, primitive_types):
                return True

            if is_dict_populated_bool:
                return True
    elif isinstance(package_dict_field, list):
        for val in package_dict_field:
            if val and isinstance(val, dict):
                is_dict_populated_bool = is_dict_populated(val)
            elif val and isinstance(val, primitive_types):
                is_dict_populated_bool = True

            if is_dict_populated_bool:
                return True

    return False
