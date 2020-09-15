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
