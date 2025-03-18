import mimetypes
from ast import literal_eval

import logging

log = logging.getLogger(__name__)


def is_data_dict_active(ddict):
    """"Returns True if data dictionary is populated"""
    for col in ddict:
        info = col.get('info', {})
        if info.get('label') or info.get('notes'):
            return True
    return False


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
    '''
    This function checks if a composite field populated. Non-composite fields will return True by default.
    '''
    composite_presets_list = ['composite', 'composite_repeating',
                              'contact_address_composite_repeating',
                              'cnra_composite_repeating']
    field_name = field.get('field_name')

    if (package_dict.get(field_name)
            and field_name != 'spatial_details'
            and field.get('preset') in composite_presets_list):
        subfield_literal_eval = {}
        try:
            subfield_literal_eval = literal_eval(package_dict[field_name])
        except (ValueError, SyntaxError) as e:
            log.debug('Unable to evaluate field {0} in package dictionary: {1}'
                      .format(field_name, package_dict.get(field_name)))

        return is_dict_populated(subfield_literal_eval)

    return True


def is_dict_populated(package_dict_field):
    '''
    Recursively checks if package dictionary field is populated.

    Since the field is a composite field, it will be nested
    with either a dictionary or list.

    Returns True if the composite field is populated
    '''
    found_populated_field = False
    exclude_keys_list = ['publicationDate']

    if isinstance(package_dict_field, (dict, list)):
        field_values = []
        if isinstance(package_dict_field, dict):
            field_values = [v for k, v in package_dict_field.items() if k not in exclude_keys_list]
        else:
            field_values = package_dict_field

        for val in field_values:
            if val and isinstance(val, dict):
                found_populated_field = is_dict_populated(val)
            elif val and isinstance(val, list):
                found_populated_field = any((is_dict_populated(x) for x in val))
            elif val:
                return True

            if found_populated_field:
                return True
    elif package_dict_field:
        return True

    return False


def guess_resource_format(url, use_mimetypes=True):
    '''
    Given a URL try to guess the best format to assign to the resource.

    The function looks for common patterns in popular geospatial services and
    file extensions, so it may not be 100% accurate. It just looks at the
    provided URL, it does not attempt to perform any remote check.

    if 'use_mimetypes' is True (default value), the mimetypes module will be
    used if no match was found before.

    Returns None if no format could be guessed.
    '''
    url = url.lower().strip()

    resource_types = {
        # OGC
        'wms': ('service=wms', 'geoserver/wms', 'mapserver/wmsserver', 'com.esri.wms.Esrimap', 'service/wms'),
        'wfs': ('service=wfs', 'geoserver/wfs', 'mapserver/wfsserver', 'com.esri.wfs.Esrimap'),
        'wcs': ('service=wcs', 'geoserver/wcs', 'imageserver/wcsserver', 'mapserver/wcsserver'),
        'sos': ('service=sos',),
        'csw': ('service=csw',),
        # ESRI
        'kml': ('mapserver/generatekml',),
        'arcims': ('com.esri.esrimap.esrimap',),
        'arcgis_rest': ('arcgis/rest/services',),
    }

    for resource_type, parts in resource_types.items():
        if any(part in url for part in parts):
            return resource_type

    file_types = {
        'kml' : ('kml',),
        'kmz': ('kmz',),
        'gml': ('gml',),
        'tif': ('tif','tiff',),
        'shp': ('shp',),
        'zip': ('zip',)
    }

    for file_type, extensions in file_types.items():
        if any(url.endswith(extension) for extension in extensions):
            return file_type

    if use_mimetypes:
        resource_format, encoding = mimetypes.guess_type(url)
        if resource_format:
            return resource_format

    return None
