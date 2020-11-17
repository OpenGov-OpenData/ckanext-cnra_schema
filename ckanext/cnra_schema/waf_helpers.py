import ckanext.cnra_schema.helpers as cnra_schema_helpers
from ckanext.spatial.harvesters.csw_fgdc import guess_resource_format

import json
import logging

log = logging.getLogger(__name__)


def get_waf_contact_values(contact_field_list):
    contact_info = {
        'contactPerson': '',
        'contactOrganization': '',
        'contactPosition': '',
        'telephone': [''],
        'email': ['']
    }
    contact_address = []

    if contact_field_list and len(contact_field_list) > 0:
        contact_field = contact_field_list[0]
        contact_info_value = contact_field.get('contact-info', {})
        contact_info = {
            'contactPerson': contact_field.get('individual-name', ''),
            'contactOrganization': contact_field.get('organisation-name', ''),
            'contactPosition': contact_field.get('position-name', ''),
            'telephone': contact_field.get('telephone', ''),
            'email': contact_info_value.get('email', '')
        }

        contact_address_list = contact_field.get('contact-address', [])
        for address in contact_address_list:
            contact_address.append({
                'addressType': address.get('addrtype', ''),
                'address': ''.join(address.get('address', '')),
                'city': address.get('city', ''),
                'state': address.get('state', ''),
                'postalCode': address.get('postal', ''),
                'country': address.get('country', '')
            })

    contact_info = json.dumps(contact_info)
    contact_address = json.dumps(contact_address)
    contact_values = {
        'contact_info': contact_info,
        'contact_address': contact_address
    }

    return contact_values


def set_waf_map_fields(package_dict, iso_values, map_fields):
    if map_fields:
        for map_field in map_fields:
            source_field = map_field.get('source')
            target_field = map_field.get('target')
            default_value = map_field.get('default')
            # If value is a list, convert to string
            value = cnra_schema_helpers.convert_list_to_string(iso_values.get(source_field, default_value), ', ')

            package_dict[target_field] = value

            # Remove from extras any keys present in the config
            cnra_schema_helpers.delete_existing_extra_from_package_dict(target_field, package_dict)

    return package_dict


def set_waf_publisher_values(package_dict, iso_values, publisher_mapping):
    publisher_field = publisher_mapping.get('publisher_field')

    if publisher_field:
        publisher_name = iso_values.get('publisher') or \
                         publisher_mapping.get('default_publisher')
        package_dict[publisher_field] = publisher_name

        # Remove from extras any keys present in the config
        cnra_schema_helpers.delete_existing_extra_from_package_dict(publisher_field, package_dict)

    return package_dict


def set_waf_contact_point(package_dict, iso_values, contact_point_mapping):
    name_field = contact_point_mapping.get('name_field')
    email_field = contact_point_mapping.get('email_field')

    if name_field:
        contact_point_name = iso_values.get('contact') or \
                           contact_point_mapping.get('default_name')
        package_dict[name_field] = contact_point_name

        # Remove from extras the name field
        cnra_schema_helpers.delete_existing_extra_from_package_dict(name_field, package_dict)

    if email_field:
        contact_point_email = iso_values.get('contact-email') or \
                            contact_point_mapping.get('default_email')
        package_dict[email_field] = contact_point_email

        # Remove from extras the email field
        cnra_schema_helpers.delete_existing_extra_from_package_dict(email_field, package_dict)

    return package_dict


def set_waf_identification_information(package_dict, iso_values):
    if iso_values.get('idinfo-citation'):
        citation = iso_values.get('idinfo-citation')
        idinfo_citation = {
            'title': citation['title'],
            'originator': citation['origin'],
            'publicationDate': citation['pubdate'],
            'edition': citation['edition'],
            'geospatialDataPresentationForm': citation['geoform'],
            # 'publisher': citation['publish'],
            'onlineLinkage': citation['onlink']
        }
        idinfo_citation = json.dumps(idinfo_citation)
        package_dict['idInfoCitation'] = idinfo_citation

        package_dict['publisher'] = citation['publish']
        if len(citation['onlink']) > 0:
            package_dict['url'] = citation['onlink'][0]

    if iso_values.get('idinfo-single-dates'):
        time_period_of_content = []
        idinfo_single_dates = iso_values.get('idinfo-single-dates')
        for item in idinfo_single_dates:
            time_period_of_content.append({
                'date': item.get('caldate', ''),
                'time': item.get('time', '')
            })
        time_period_of_content = json.dumps(time_period_of_content)
        package_dict['timePeriodOfContent'] = time_period_of_content

    beginning_period = iso_values.get('temporal-extent-begin', [])
    package_dict['beginningTimePeriodOfContent'] = cnra_schema_helpers.get_date_and_time_dict(beginning_period)

    ending_period = iso_values.get('temporal-extent-end', [])
    package_dict['endingTimePeriodOfContent'] = cnra_schema_helpers.get_date_and_time_dict(ending_period)

    limitations = cnra_schema_helpers.convert_list_to_string(iso_values.get('access-constraints', ''))
    package_dict['limitations'] = limitations

    package_dict['purpose'] = iso_values.get('purpose')
    package_dict['maintenanceAndUpdateFrequency'] = iso_values.get('frequency-of-update', '')

    iso_use_constraints = cnra_schema_helpers.convert_list_to_string(iso_values.get('use-constraints', ''))
    iso_limitations_on_public_access = cnra_schema_helpers.convert_list_to_string(iso_values.get('limitations-on-public-access', ''))

    use_constraints = iso_use_constraints + ' ' + iso_limitations_on_public_access
    package_dict['useConstraints'] = use_constraints

    return package_dict


def set_waf_keywords(package_dict, iso_values):
    keywords = iso_values.get('keywords', [])
    theme_keywords = []
    place_keywords = []
    stratum_keywords = []
    temporal_keywords = []
    taxon_keywords = []

    if keywords and len(keywords) > 0:
        for keyword_dict in keywords:
            keyword_type = keyword_dict['type']
            keyword_list = keyword_dict.get('keyword', [])
            if keyword_type == 'theme':
                theme_keywords = theme_keywords + keyword_list
            elif keyword_type == 'place':
                place_keywords = place_keywords + keyword_list
            elif keyword_type == 'stratum':
                stratum_keywords = stratum_keywords + keyword_list
            elif keyword_type == 'temporal':
                temporal_keywords = temporal_keywords + keyword_list
            elif keyword_type == 'taxon':
                taxon_keywords = taxon_keywords + keyword_list
            else:
                continue

    package_dict['themeKeywords'] = cnra_schema_helpers.convert_list_to_string(theme_keywords, ', ')
    package_dict['placeKeywords'] = cnra_schema_helpers.convert_list_to_string(place_keywords, ', ')
    package_dict['stratumKeywords'] = cnra_schema_helpers.convert_list_to_string(stratum_keywords, ', ')
    package_dict['temporalKeywords'] = cnra_schema_helpers.convert_list_to_string(temporal_keywords, ', ')
    package_dict['taxonKeywords'] = cnra_schema_helpers.convert_list_to_string(taxon_keywords, ', ')

    return package_dict


def set_waf_geologic_information(package_dict, iso_values):
    if iso_values.get('geologic-age'):
        geologic_age = []
        geologic_age_list = iso_values.get('geologic-age', [])
        for age in geologic_age_list:
            geologic_age.append({
                'geologicTimeScale': age.get('geologic-time-scale', ''),
                'geologicAgeEstimate': age.get('geologic-age-estimate', ''),
                'geologicAgeUncertainty': age.get('geologic-age-uncertainty', ''),
                'geologicAgeExplanation': age.get('geologic-age-explanation', '')
            })
        geologic_age = json.dumps(geologic_age)
        package_dict['geologicAge'] = geologic_age

    if iso_values.get('beginning-geologic-age'):
        beginning_geologic_age_values = iso_values.get('beginning-geologic-age')
        beginning_geologic_age = {
            'geologicTimeScale': beginning_geologic_age_values.get('geologic-time-scale', ''),
            'geologicAgeEstimate': beginning_geologic_age_values.get('geologic-age-estimate', ''),
            'geologicAgeUncertainty': beginning_geologic_age_values.get('geologic-age-uncertainty', ''),
            'geologicAgeExplanation': beginning_geologic_age_values.get('geologic-age-explanation', '')
        }
        beginning_geologic_age = json.dumps(beginning_geologic_age)
        package_dict['beginningGeologicAge'] = beginning_geologic_age

    if iso_values.get('ending-geologic-age'):
        ending_geologic_age_values = iso_values.get('ending-geologic-age')
        ending_geologic_age = {
            'geologicTimeScale': ending_geologic_age_values.get('geologic-time-scale', ''),
            'geologicAgeEstimate': ending_geologic_age_values.get('geologic-age-estimate', ''),
            'geologicAgeUncertainty': ending_geologic_age_values.get('geologic-age-uncertainty', ''),
            'geologicAgeExplanation': ending_geologic_age_values.get('geologic-age-explanation', '')
        }
        ending_geologic_age = json.dumps(ending_geologic_age)
        package_dict['endingGeologicAge'] = ending_geologic_age

    if iso_values.get('geologic-citation'):
        citation = iso_values.get('geologic-citation')
        geologic_citation = {
            'title': citation['title'],
            'originator': citation['origin'],
            'publicationDate': citation['pubdate'],
            'geospatialDataPresentationForm': citation['geoform'],
            'sername': citation['sername'],
            'issue': citation['issue'],
            'onlineLinkage': citation['onlink']
        }
        geologic_citation = json.dumps(geologic_citation)
        package_dict['geologicCitation'] = geologic_citation

    if iso_values.get('geographic-extent-description'):
        package_dict['geographicExtentDescription'] = iso_values['geographic-extent-description']

    return package_dict


def set_waf_bounding_information(package_dict, iso_values):
    # Bounding coordinates
    bbox = {}
    if iso_values.get('bbox', '') and len(iso_values['bbox']) > 0:
        bbox = iso_values['bbox'][0]
    bounding_coordinate = {
        'northBoundingCoordinate': bbox.get('north', ''),
        'eastBoundingCoordinate': bbox.get('east', ''),
        'southBoundingCoordinate': bbox.get('south', ''),
        'westBoundingCoordinate': bbox.get('west', '')
    }
    bounding_coordinate = json.dumps(bounding_coordinate)
    package_dict['boundingCoordinate'] = bounding_coordinate

    # Bounding altitudes
    if iso_values.get('bounding-altitude'):
        b_altitude = {}
        if len(iso_values['bounding-altitude']) > 0:
            b_altitude = iso_values['bounding-altitude'][0]
        bounding_altitudes = {
            'altitudeMinimum': b_altitude.get('minimum-altitude', ''),
            'altitudeMaximum': b_altitude.get('maximum-altitude', ''),
            'altitudeDistanceUnits': b_altitude.get('altitude-units', '')
        }
        bounding_altitudes = json.dumps(bounding_altitudes)
        package_dict['boundingAltitudes'] = bounding_altitudes

    return package_dict


def set_waf_citations(package_dict, iso_values):
    if iso_values.get('classsys-citation'):
        citation = iso_values.get('classsys-citation')
        classsys_citation = {
            'originator': citation['origin'],
        }
        classsys_citation = json.dumps(classsys_citation)
        package_dict['classSysCitation'] = classsys_citation

    if iso_values.get('idref-citation'):
        citation = iso_values.get('idref-citation')
        idref_citation = {
            'originator': citation['origin'],
        }
        idref_citation = json.dumps(idref_citation)
        package_dict['idRefCitation'] = idref_citation

    return package_dict


def set_waf_contacts(package_dict, iso_values):
    if iso_values.get('ider-contact'):
        ider_contact = get_waf_contact_values(iso_values['ider-contact'])
        package_dict['iderContact'] = ider_contact.get('contact_info')
        package_dict['iderContactAddress'] = ider_contact.get('contact_address')

    if iso_values.get('vouchers-contact'):
        vouchers_contact = get_waf_contact_values(iso_values['vouchers-contact'])
        package_dict['vouchersContact'] = vouchers_contact.get('contact_info')
        package_dict['vouchersContactAddress'] = vouchers_contact.get('contact_address')

    if iso_values.get('vouchers-specimen'):
        package_dict['vouchersSpecimen'] = iso_values['vouchers-specimen']

    distributor_contact = get_waf_contact_values(iso_values.get('distributor', []))
    package_dict['distributorContact'] = distributor_contact.get('contact_info')
    package_dict['distributorContactAddress'] = distributor_contact.get('contact_address')

    metadata_contact = get_waf_contact_values(iso_values.get('metadata-point-of-contact', []))
    package_dict['metadataContact'] = metadata_contact.get('contact_info')
    package_dict['metadataContactAddress'] = metadata_contact.get('contact_address')

    return package_dict


def set_waf_data_quality_information(package_dict, iso_values):
    # (2) Data_Quality_Information

    if iso_values.get('attribute-accuracy-report'):
        package_dict['attributeAccuracyReport'] = iso_values['attribute-accuracy-report']

    if iso_values.get('completeness-report'):
        package_dict['completenessReport'] = iso_values['completeness-report']

    if iso_values.get('lineage-citation'):
        citation = iso_values.get('lineage-citation')
        lineage_citation = {
            'title': citation['title'],
            'originator': citation['origin'],
            'publicationDate': citation['pubdate'],
            # 'edition': citation['edition'],
            'geospatialDataPresentationForm': citation['geoform'],
            # 'publisher': citation['publish'],
            # 'onlineLinkage': citation['onlink']
        }
        lineage_citation = json.dumps(lineage_citation)
        package_dict['lineageCitation'] = lineage_citation

    if iso_values.get('source-scale-denominator'):
        package_dict['sourceScaleDenominator'] = iso_values['source-scale-denominator']

    if iso_values.get('type-of-source-media'):
        package_dict['typeOfSourceMedia'] = iso_values['type-of-source-media']

    if iso_values.get('source-currentness-reference'):
        package_dict['sourceCurrentnessReference'] = iso_values['source-currentness-reference']

    if iso_values.get('source-citation-abbreviation'):
        package_dict['sourceCitationAbbreviation'] = iso_values['source-citation-abbreviation']

    if iso_values.get('distribution-liability'):
        package_dict['distributionLiability'] = iso_values['distribution-liability']

    return package_dict


def set_waf_spatial_reference_information(package_dict, iso_values):
    ## (4) Spatial_Reference_Information

    if iso_values.get('map-projection-name'):
        package_dict['mapProjectionName'] = iso_values['map-projection-name']

    if iso_values.get('planar-coordinate-information'):
        coordinate_information = iso_values.get('planar-coordinate-information')
        planar_coordinate_information = {
            'planarCoordinateEncodingMethod': coordinate_information['planar-coordinate-encoding-method'],
            'abscissaResolution': coordinate_information['abscissa-resolution'],
            'ordinateResolution': coordinate_information['ordinate-resolution'],
            'planarDistanceUnits': coordinate_information['planar-distance-units']
        }
        planar_coordinate_information = json.dumps(planar_coordinate_information)
        package_dict['planarCoordinateInformation'] = planar_coordinate_information

    if iso_values.get('horizontal-datum-name'):
        package_dict['horizontalDatumName'] = iso_values['horizontal-datum-name']

    return package_dict


def set_metadata_reference_information(package_dict, iso_values):
    # (7) Metadata_Reference_Information
    # Resources
    ea_list = iso_values.get('entity-and-attribute', [])
    resource_locators = iso_values.get('resource-locator', [])

    if len(resource_locators):
        resources = []
        for index, resource_locator in enumerate(resource_locators):
            url = resource_locator.get('url', '').strip()
            if url:
                resource = {}
                res_name = resource_locator.get('format-name', 'Unnamed resource')
                res_description = resource_locator.get('format-info-content', '')
                if len(ea_list) > 0 and index < len(ea_list):
                    ea_info = ea_list[index]
                    res_name = ea_info.get('entity-type-label')
                    res_description = ea_info.get('entity-type-definition')
                    attribute_list = ea_info.get('attribute', [])
                    attribute = []
                    for item in attribute_list:
                        attribute.append({
                            'attributeLabel': item.get('attribute-label', ''),
                            'attributeDefinition': item.get('attribute-definition', ''),
                        })
                    attribute = json.dumps(attribute)
                    resource['attribute'] = attribute

                res_format = guess_resource_format(url)
                if not res_format:
                    res_format = guess_resource_format(res_name)
                resource['format'] = res_format

                resource.update({
                    'url': url,
                    'name': res_name,
                    'description': res_description,
                    'url_type': 'xloader',
                })
                resources.append(resource)
        package_dict['resources'] = resources

    return package_dict
