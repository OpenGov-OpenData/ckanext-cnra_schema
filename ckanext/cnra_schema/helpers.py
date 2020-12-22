from ast import literal_eval

import logging

log = logging.getLogger(__name__)


def composite_repeating_get_formatted_contact_address_dict(package_dict_field):
    address_line1 = package_dict_field['address']
    address_line2 = '{0}, {1} {2}'.format(package_dict_field['city'], package_dict_field['state'],
                                          package_dict_field['postalCode'])
    address_line3 = package_dict_field['country']

    address_dict = {
        'addressLine1': address_line1,
        'addressLine2': address_line2,
        'addressLine3': address_line3
    }

    return address_dict


def is_composite_field_populated(package_dict, field):
    """"
    This function checks if a composite field populated. Non-composite fields will return True by default.
    """
    field_name = field.get('field_name')

    if package_dict.get(field_name) and field_name not in 'spatial_details' \
            and field.get('preset') in ['composite', 'composite_repeating', 'contact_address_composite_repeating',
                                        'cnra_composite_repeating']:

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
