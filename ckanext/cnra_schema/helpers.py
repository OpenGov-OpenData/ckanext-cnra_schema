import logging

log = logging.getLogger(__name__)


def get_extra(key, package_dict):
    for extra in package_dict.get('extras', []):
        if extra['key'] == key:
            return extra


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
            existing_extra = get_extra(target_field, package_dict)
            if existing_extra:
                package_dict['extras'].remove(existing_extra)

    return package_dict


def set_waf_publisher_values(package_dict, iso_values, publisher_mapping):
    publisher_field = publisher_mapping.get('publisher_field')

    if publisher_field:
        publisher_name = iso_values.get('publisher') or \
                         publisher_mapping.get('default_publisher')
        package_dict[publisher_field] = publisher_name

        # Remove from extras any keys present in the config
        existing_extra = get_extra(publisher_field, package_dict)
        if existing_extra:
            package_dict['extras'].remove(existing_extra)

    return package_dict


def set_waf_contact_point(package_dict, iso_values, contact_point_mapping):
    name_field = contact_point_mapping.get('name_field')
    email_field = contact_point_mapping.get('email_field')

    if name_field:
        contact_point_name = iso_values.get('contact') or \
                           contact_point_mapping.get('default_name')
        package_dict[name_field] = contact_point_name

        # Remove from extras the name field
        existing_extra = get_extra(name_field, package_dict)
        if existing_extra:
            package_dict['extras'].remove(existing_extra)

    if email_field:
        contact_point_email = iso_values.get('contact-email') or \
                            contact_point_mapping.get('default_email')
        package_dict[email_field] = contact_point_email

        # Remove from extras the email field
        existing_extra = get_extra(email_field, package_dict)
        if existing_extra:
            package_dict['extras'].remove(existing_extra)

    return package_dict
