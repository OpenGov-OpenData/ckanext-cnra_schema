from ckan.plugins import toolkit, IConfigurer, SingletonPlugin, implements
from ckanext.spatial.interfaces import ISpatialHarvester
from ckanext.spatial.harvesters.csw_fgdc import guess_resource_format
import json
from markupsafe import Markup

import logging
log = logging.getLogger(__name__)

class cnraSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(ISpatialHarvester, inherit=True)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")

        config['scheming.presets'] = """
ckanext.scheming:presets.json
ckanext.repeating:presets.json
ckanext.composite:presets.json
"""

        config['scheming.dataset_schemas'] = """
ckanext.cnra_schema:schemas/dataset.yaml
"""

    def get_package_dict(self, context, data_dict):
        harvest_object = data_dict['harvest_object']
        harvest_source_type = harvest_object.source.type

        if harvest_source_type == 'fgdc':
            modified_package_dict = self.get_fgdc_package_dict(data_dict)

        elif harvest_source_type == 'waf':
            modified_package_dict = self.get_waf_package_dict(data_dict)
        
        return modified_package_dict


    def get_fgdc_package_dict(self, data_dict):
        package_dict = data_dict['package_dict']
        fgdc_values = data_dict['fgdc_values']

        contact = 'None'
        contact_email = 'None'
        if fgdc_values.get('contact'):
            contact = fgdc_values['contact']
        if fgdc_values.get('contact-email'):
            contact_email = ', '.join(fgdc_values['contact-email'])
        package_dict['contact_name'] = contact
        package_dict['contact_email'] = contact_email
        package_dict['public_access_level'] = 'Public'

        ## (1) Identification_Information

        if fgdc_values.get('idinfo-citation'):
            citation = fgdc_values.get('idinfo-citation')
            idinfo_citation = {
                'title': citation['title'],
                'originator': citation['origin'],
                'publicationDate': citation['pubdate'],
                'edition': citation['edition'],
                'geospatialDataPresentationForm': citation['geoform'],
                #'publisher': citation['publish'],
                'onlineLinkage': citation['onlink']
            }
            idinfo_citation = json.dumps(idinfo_citation)
            package_dict['idInfoCitation'] = idinfo_citation

            package_dict['publisher'] = citation['publish']
            if len(citation['onlink']) > 0:
                package_dict['url'] = citation['onlink'][0]

        package_dict['purpose'] = fgdc_values.get('purpose')

        if fgdc_values.get('idinfo-single-dates'):
            time_period_of_content = []
            idinfo_single_dates = fgdc_values.get('idinfo-single-dates')
            for item in idinfo_single_dates:
                time_period_of_content.append({
                    'date': item.get('caldate',''),
                    'time': item.get('time','')
                })
            time_period_of_content = json.dumps(time_period_of_content)
            package_dict['timePeriodOfContent'] = time_period_of_content

        if fgdc_values.get('idinfo-range-of-dates'):
            idinfo_period = fgdc_values.get('idinfo-range-of-dates')
            beginning_period = {
                'date': idinfo_period.get('begdate',''),
                'time': idinfo_period.get('begtime','')
            }
            ending_period = {
                'date': idinfo_period.get('enddate',''),
                'time': idinfo_period.get('endtime','')
            }
            beginning_period = json.dumps(beginning_period)
            ending_period = json.dumps(ending_period)
            package_dict['beginningTimePeriodOfContent'] = beginning_period
            package_dict['endingTimePeriodOfContent'] = ending_period

        if fgdc_values.get('geologic-age'):
            geologic_age = []
            geologic_age_list = fgdc_values.get('geologic-age', [])
            for age in geologic_age_list:
                geologic_age.append({
                    'geologicTimeScale': age.get('geologic-time-scale',''),
                    'geologicAgeEstimate': age.get('geologic-age-estimate',''),
                    'geologicAgeUncertainty': age.get('geologic-age-uncertainty',''),
                    'geologicAgeExplanation': age.get('geologic-age-explanation','')
                })
            geologic_age = json.dumps(geologic_age)
            package_dict['geologicAge'] = geologic_age

        if fgdc_values.get('beginning-geologic-age'):
            beginning_geologic_age = {
                'geologicTimeScale': fgdc_values.get('geologic-time-scale',''),
                'geologicAgeEstimate': fgdc_values.get('geologic-age-estimate',''),
                'geologicAgeUncertainty': fgdc_values.get('geologic-age-uncertainty',''),
                'geologicAgeExplanation': fgdc_values.get('geologic-age-explanation','')
            }
            beginning_geologic_age = json.dumps(beginning_geologic_age)
            package_dict['beginningGeologicAge'] = beginning_geologic_age

        if fgdc_values.get('ending-geologic-age'):
            ending_geologic_age = {
                'geologicTimeScale': fgdc_values.get('geologic-time-scale',''),
                'geologicAgeEstimate': fgdc_values.get('geologic-age-estimate',''),
                'geologicAgeUncertainty': fgdc_values.get('geologic-age-uncertainty',''),
                'geologicAgeExplanation': fgdc_values.get('geologic-age-explanation','')
            }
            ending_geologic_age = json.dumps(ending_geologic_age)
            package_dict['endingGeologicAge'] = ending_geologic_age

        if fgdc_values.get('geologic-citation'):
            citation = fgdc_values.get('geologic-citation')
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

        package_dict['currentnessReference'] = fgdc_values.get('current')
        package_dict['progress'] = fgdc_values.get('progress')
        package_dict['maintenanceAndUpdateFrequency'] = fgdc_values.get('update')
        package_dict['geographicExtentDescription'] = fgdc_values['geographic-extent-description']

        # Bounding coordinates
        bbox = {}
        if len(fgdc_values['bbox']) > 0:
            bbox = fgdc_values['bbox'][0]
        bounding_coordinate = {
            'northBoundingCoordinate': bbox.get('north',''),
            'eastBoundingCoordinate': bbox.get('east',''),
            'southBoundingCoordinate': bbox.get('south',''),
            'westBoundingCoordinate': bbox.get('west','')
        }
        bounding_coordinate = json.dumps(bounding_coordinate)
        package_dict['boundingCoordinate'] = bounding_coordinate

        # Bounding altitudes
        b_altitude = {}
        if len(fgdc_values['bounding-altitude']) > 0:
            b_altitude = fgdc_values['bounding-altitude'][0]
        bounding_altitudes = {
            'altitudeMinimum': b_altitude.get('minimum-altitude',''),
            'altitudeMaximum': b_altitude.get('maximum-altitude',''),
            'altitudeDistanceUnits': b_altitude.get('altitude-units','')
        }
        bounding_altitudes = json.dumps(bounding_altitudes)
        package_dict['boundingAltitudes'] = bounding_altitudes

        package_dict['themeKeywords'] = ', '.join(fgdc_values['theme-keywords'])
        package_dict['placeKeywords'] = ', '.join(fgdc_values['place-keywords'])
        package_dict['stratumKeywords'] = ', '.join(fgdc_values['stratum-keywords'])
        package_dict['temporalKeywords'] = ', '.join(fgdc_values['temporal-keywords'])

        package_dict['taxonKeywords'] = ', '.join(fgdc_values['taxon-keywords'])

        if fgdc_values.get('classsys-citation'):
            citation = fgdc_values.get('classsys-citation')
            classsys_citation = {
                'originator': citation['origin'],
            }
            classsys_citation = json.dumps(classsys_citation)
            package_dict['classSysCitation'] = classsys_citation

        if fgdc_values.get('idref-citation'):
            citation = fgdc_values.get('idref-citation')
            idref_citation = {
                'originator': citation['origin'],
            }
            idref_citation = json.dumps(idref_citation)
            package_dict['idRefCitation'] = idref_citation

        ider_contact = self.get_contact_values(fgdc_values, 'ider-contact')
        package_dict['iderContact'] = ider_contact.get('contact_info')
        package_dict['iderContactAddress'] = ider_contact.get('contact_address')

        vouchers_contact = self.get_contact_values(fgdc_values, 'vouchers-contact')
        package_dict['vouchersContact'] = vouchers_contact.get('contact_info')
        package_dict['vouchersContactAddress'] = vouchers_contact.get('contact_address')

        package_dict['vouchersSpecimen'] = fgdc_values['vouchers-specimen']

        #package_dict['accessConstraints'] = fgdc_values['access-constraints']
        package_dict['limitations'] = fgdc_values['access-constraints']
        package_dict['useConstraints'] = fgdc_values['use-constraints']

        point_of_contact = self.get_contact_values(fgdc_values, 'point-of-contact')
        package_dict['pointOfContact'] = point_of_contact.get('contact_info')
        package_dict['pointOfContactAddress'] = point_of_contact.get('contact_address')

        package_dict['credit'] = fgdc_values['credit']
        package_dict['nativeDatasetEnvironment'] = fgdc_values['native-dataset-environment']

        ## (2) Data_Quality_Information

        package_dict['attributeAccuracyReport'] = fgdc_values['attribute-accuracy-report']
        package_dict['completenessReport'] = fgdc_values['completeness-report']

        if fgdc_values.get('lineage-citation'):
            citation = fgdc_values.get('lineage-citation')
            lineage_citation = {
                'title': citation['title'],
                'originator': citation['origin'],
                'publicationDate': citation['pubdate'],
                #'edition': citation['edition'],
                'geospatialDataPresentationForm': citation['geoform'],
                #'publisher': citation['publish'],
                #'onlineLinkage': citation['onlink']
            }
            lineage_citation = json.dumps(lineage_citation)
            package_dict['lineageCitation'] = lineage_citation

        package_dict['sourceScaleDenominator'] = fgdc_values['source-scale-denominator']
        package_dict['typeOfSourceMedia'] = fgdc_values['type-of-source-media']
        package_dict['sourceCurrentnessReference'] = fgdc_values['source-currentness-reference']
        package_dict['sourceCitationAbbreviation'] = fgdc_values['source-citation-abbreviation']

        ## (4) Spatial_Reference_Information

        package_dict['mapProjectionName'] = fgdc_values['map-projection-name']

        if fgdc_values.get('planar-coordinate-information'):
            coordinate_information = fgdc_values.get('planar-coordinate-information')
            planar_coordinate_information = {
                'planarCoordinateEncodingMethod': coordinate_information['planar-coordinate-encoding-method'],
                'abscissaResolution': coordinate_information['abscissa-resolution'],
                'ordinateResolution': coordinate_information['ordinate-resolution'],
                'planarDistanceUnits': coordinate_information['planar-distance-units']
            }
            planar_coordinate_information = json.dumps(planar_coordinate_information)
            package_dict['planarCoordinateInformation'] = planar_coordinate_information

        package_dict['horizontalDatumName'] = fgdc_values['horizontal-datum-name']

        ## (6) Distribution_Information

        distributor_contact = self.get_contact_values(fgdc_values, 'distributor')
        package_dict['distributorContact'] = distributor_contact.get('contact_info')
        package_dict['distributorContactAddress'] = distributor_contact.get('contact_address')

        package_dict['distributionLiability'] = fgdc_values['distribution-liability']

        ## (7) Metadata_Reference_Information

        metadata_contact = self.get_contact_values(fgdc_values, 'metadata-contact')
        package_dict['metadataContact'] = metadata_contact.get('contact_info')
        package_dict['metadataContactAddress'] = metadata_contact.get('contact_address')

        ## Resources

        ea_list = fgdc_values.get('entity-and-attribute', [])
        resource_locators = fgdc_values.get('resource-locator', [])

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
                                'attributeLabel': item.get('attribute-label',''),
                                'attributeDefinition': item.get('attribute-definition',''),
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


    def get_contact_values(self, fgdc_values, fgdc_field):
        contact_info = {
            'contactPerson': '',
            'contactOrganization': '',
            'contactPosition': '',
            'telephone': [''],
            'email': [''],
            #'fax': [''],
            #'hoursOfService': '',
            #'contactInstructions': '',
        }
        contact_address = []

        if fgdc_values.get(fgdc_field):
            contact = fgdc_values.get(fgdc_field)
            contact_info = {
                'contactPerson': contact.get('individual-name'),
                'contactOrganization': contact.get('organisation-name'),
                'contactPosition': contact.get('position-name'),
                'telephone': contact.get('telephone'),
                'email': contact.get('email'),
                #'fax': contact.get('fax'),
                #'hoursOfService': contact.get('hours-of-service'),
                #'contactInstructions': contact.get('contact-instructions'),
            }

            contact_address_list = contact.get('contact-address',[])
            for address in contact_address_list:
                contact_address.append({
                    'addressType': address.get('addrtype'),
                    'address': ', '.join(address.get('address')),
                    'city': address.get('city'),
                    'state': address.get('state'),
                    'postalCode': address.get('postal'),
                    'country': address.get('country')
                })

        contact_info = json.dumps(contact_info)
        contact_address = json.dumps(contact_address)
        contact_values = {
            'contact_info': contact_info,
            'contact_address': contact_address
        }

        return(contact_values)


    def get_waf_package_dict(self, data_dict):
        harvest_object = data_dict['harvest_object']
        config_str = harvest_object.job.source.config
        harvest_job_config = json.loads(config_str)

        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']

        def get_extra(key, package_dict):
            for extra in package_dict.get('extras', []):
                if extra['key'] == key:
                    return extra

        if not 'extras' in package_dict:
            package_dict['extras'] = []

        # set the mapping fields its corresponding default_values
        map_fields = harvest_job_config.get('map_fields', [])
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

        # set the publisher
        publisher_mapping = harvest_job_config.get('publisher', {})
        publisher_field = publisher_mapping.get('publisher_field')
        if publisher_field:
            publisher_name = iso_values.get('publisher') or \
                             publisher_mapping.get('default_publisher')
            package_dict[publisher_field] = publisher_name
            # Remove from extras any keys present in the config
            existing_extra = get_extra(publisher_field, package_dict)
            if existing_extra:
                package_dict['extras'].remove(existing_extra)

        # set the contact point
        contact_point_mapping = harvest_job_config.get('contact_point', {})
        name_field = contact_point_mapping.get('name_field')
        email_field = contact_point_mapping.get('email_field')

        if name_field:
            contactPointName = iso_values.get('contact') or \
                               contact_point_mapping.get('default_name')
            package_dict[name_field] = contactPointName
            # Remove from extras the name field
            existing_extra = get_extra(name_field, package_dict)
            if existing_extra:
                package_dict['extras'].remove(existing_extra)

        if email_field:
            contactPointEmail = iso_values.get('contact-email') or \
                                contact_point_mapping.get('default_email')
            package_dict[email_field] = contactPointEmail
            # Remove from extras the email field
            existing_extra = get_extra(email_field, package_dict)
            if existing_extra:
                package_dict['extras'].remove(existing_extra)

        log.debug(iso_values)

        log.debug(package_dict)

        return package_dict