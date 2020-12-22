import ckanext.cnra_schema.waf_utils as waf_harvest_utils
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false


class TestWAFHelperFunctions(object):

    assert_dict_equal.__self__.maxDiff = None

    def test_set_waf_map_fields_from_source_values(self):
        package_dict = {}
        map_fields = [{
            'default': 'English',
            'source': 'language',
            'target': 'language'
        }]
        iso_values = {'language': 'Spanish'}
    
        modified_package_dict = waf_harvest_utils.set_waf_map_fields(package_dict, iso_values, map_fields)
    
        assert_equal('Spanish', modified_package_dict.get('language'))

    def test_set_waf_map_fields_from_default_values(self):
        package_dict = {}
        map_fields = [{
            'default': 'English',
            'source': 'language',
            'target': 'language'
        }]
        iso_values = {}
    
        modified_package_dict = waf_harvest_utils.set_waf_map_fields(package_dict, iso_values, map_fields)
    
        assert_equal('English', modified_package_dict.get('language'))
    
    def test_set_waf_map_fields_multi_value_map_field(self):
        package_dict = {}
        map_fields = [
            {
                'default': 'English',
                'source': 'language',
                'target': 'language',
            },
            {
                'default': 'Canada',
                'source': 'spatial',
                'target': 'spatial_coverage'
            }
        ]
        iso_values = {}
    
        modified_package_dict = waf_harvest_utils.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)
    
        assert_dict_equal({'language': 'English', 'spatial_coverage': 'Canada'}, modified_package_dict)
    
    def test_set_waf_map_fields_value_is_list(self):
        package_dict = {}
        map_fields = [{
            'default': '00',
            'source': 'coordinate',
            'target': 'coordinate'
        }]
        iso_values = {'coordinate': ['-75.57563781738281', '-69.82928466796875']}
    
        modified_package_dict = waf_harvest_utils.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)
    
        assert_equal('-75.57563781738281, -69.82928466796875', modified_package_dict.get('coordinate'))
    
    def test_set_waf_map_fields_empty_map_field(self):
        package_dict = {}
        map_fields = []
        iso_values = {}
        modified_package_dict = waf_harvest_utils.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)
    
        assert_dict_equal({}, package_dict)

    def test_set_waf_publisher_values_from_iso_values(self):
        package_dict = {}
        publisher_mapping = {'publisher_field': 'publisher', 'default_publisher': 'Default-Publisher'}
        iso_values = {'publisher': 'Test-User'}
        modified_package_dict = waf_harvest_utils.set_waf_publisher_values(package_dict, iso_values, publisher_mapping)
    
        assert_equal('Test-User', modified_package_dict.get('publisher'))

    def test_set_waf_publisher_values_from_harvest_job_config(self):
        package_dict = {}
        publisher_mapping = {'publisher_field': 'publisher', 'default_publisher': 'Default-Publisher'}
        iso_values = {}
        modified_package_dict = waf_harvest_utils.set_waf_publisher_values(package_dict, iso_values,
                                                                             publisher_mapping)
    
        assert_equal('Default-Publisher', modified_package_dict.get('publisher'))
    
    def test_set_waf_publisher_values_empty_publisher_mapping(self):
        package_dict = {}
        publisher_mapping = {}
        iso_values = {}
        modified_package_dict = waf_harvest_utils.set_waf_publisher_values(package_dict, iso_values,
                                                                             publisher_mapping)
    
        assert_dict_equal({}, package_dict)

    def test_set_waf_contact_point_from_iso_values(self):
        package_dict = {}
        contact_point_mapping = {
            'default_email': 'test@default.com',
            'name_field': 'contact_name',
            'default_name': 'Default Name',
            'email_field': 'contact_email'
        }
        iso_values = {'contact': 'John Smith', 'contact-email': 'test@test.com'}
        modified_package_dict = waf_harvest_utils.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)
    
        assert_dict_equal({'contact_name': 'John Smith', 'contact_email': 'test@test.com'}, package_dict)
    
    def test_set_waf_contact_point_from_default_values(self):
        package_dict = {}
        contact_point_mapping = {
            'default_email': 'test@default.com',
            'name_field': 'contact_name',
            'default_name': 'Default Name',
            'email_field': 'contact_email'
        }
        iso_values = {}
        modified_package_dict = waf_harvest_utils.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)
    
        assert_equal({'contact_name': 'Default Name', 'contact_email': 'test@default.com'}, package_dict)
    
    def test_set_waf_contact_point_empty_mapping(self):
        package_dict = {}
        contact_point_mapping = {}
        iso_values = {}
        modified_package_dict = waf_harvest_utils.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)
    
        assert_dict_equal({}, package_dict)

    def test_set_waf_identification_information_success_default_iso_values(self):
        iso_values = {
            'temporal-extent-begin': [
                '2012-01-01'
            ],
            'temporal-extent-end': [
                '2015-01-01'
            ],
            'access-constraints': [
                'otherRestrictions'
            ],
            'purpose': 'We collected these data to examine the rangewide population genetic structure, measure '
                       'genetic diversity and differentiation among populations, and identify sites that may '
                       'represent introduced populations of the Santa Ana sucker Catostomus santaanae, an ICUN '
                       'endangered species. These data provide key genetic information for informing recovery efforts.',
            'frequency-of-update': 'irregular',
            'use-constraints': [
                'Unless otherwise stated, all data, metadata and related materials are considered to satisfy the '
                'quality standards relative to the purpose for which the data were collected. Although these data '
                'and associated metadata have been reviewed for accuracy and completeness and approved for release by'
                ' the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or '
                'utility of the data on any other system or for general or scientific purposes, nor shall the act of '
                'distribution constitute any such warranty. Any use of trade, firm, or product names is for '
                'descriptive purposes only and does not imply endorsement by the U.S. Government.'
            ],
            'limitations-on-public-access': [
                'Use Constraints: The authors of these data require that users direct any questions pertaining to '
                'appropriate use or assistance with understanding limitations and interpretation of the data to the '
                'individuals/organization listed in the Point of Contact section.',
                'Access Constraints: none'
            ]
        }
        package_dict = waf_harvest_utils.set_waf_identification_information({}, iso_values)

        assert_dict_equal(package_dict,
                          {
                            'beginningTimePeriodOfContent': '{\"date\": \"2012-01-01\", \"time\": \"\"}',
                            'endingTimePeriodOfContent': '{\"date\": \"2015-01-01\", \"time\": \"\"}',
                            'limitations': 'otherRestrictions',
                            'purpose': 'We collected these data to examine the rangewide population genetic structure, '
                                       'measure genetic diversity and differentiation among populations, and identify '
                                       'sites that may represent introduced populations of the Santa Ana sucker '
                                       'Catostomus santaanae, an ICUN endangered species. These data provide key '
                                       'genetic information for informing recovery efforts.',
                            'maintenanceAndUpdateFrequency': 'irregular',
                            'useConstraints': 'Unless otherwise stated, all data, metadata and related materials are '
                                              'considered to satisfy the quality standards relative to the purpose for '
                                              'which the data were collected. Although these data and associated '
                                              'metadata have been reviewed for accuracy and completeness and approved '
                                              'for release by the U.S. Geological Survey (USGS), no warranty expressed '
                                              'or implied is made regarding the display or utility of the data on any '
                                              'other system or for general or scientific purposes, nor shall the act '
                                              'of distribution constitute any such warranty. Any use of trade, firm, '
                                              'or product names is for descriptive purposes only and does not imply '
                                              'endorsement by the U.S. Government. Use Constraints: The authors of '
                                              'these data require that users direct any questions pertaining to '
                                              'appropriate use or assistance with understanding limitations and '
                                              'interpretation of the data to the individuals/organization listed in '
                                              'the Point of Contact section. Access Constraints: none'

                          })

    def test_set_waf_identification_information_success_with_identification_fields(self):
        iso_values = {
            'idinfo-citation': {
                'origin': [
                    'Richmond, J.Q.',
                    'Backlin, A.R.',
                    'Galst-Cavalcante, Carey',
                    'O\u2019Brien, J.W.',
                    'Fisher, R.N.',
                    'Jonathan Q. Richmond',
                    'Adam R. Backlin',
                    'Carey Galst-Cavalcante',
                    'John W O\"Brien',
                    'Robert N. Fisher'
                ],
                'othercit': '',
                'pubdate': '20170101',
                'title': 'Microsatellite genotype scores for a contemporary, range-wide sample of Santa Ana sucker in '
                         'southern California',
                'pubplace': '',
                'publish': '',
                'edition': '',
                'geoform': '',
                'sername': '',
                'onlink': [

                ],
                "issue": ""
            }
        }
        package_dict = waf_harvest_utils.set_waf_identification_information({}, iso_values)

        assert_dict_equal(package_dict,
                          {'beginningTimePeriodOfContent': '{"date": "", "time": ""}',
                           'endingTimePeriodOfContent': '{"date": "", "time": ""}',
                           'idInfoCitation': '{"originator": ["Richmond, J.Q.", "Backlin, A.R.", "Galst-Cavalcante, '
                                             'Carey", "O\\\\u2019Brien, J.W.", "Fisher, R.N.", "Jonathan Q. Richmond", '
                                             '"Adam R. Backlin", "Carey Galst-Cavalcante", "John W O\\"Brien", "Robert '
                                             'N. Fisher"], "onlineLinkage": [], "title": "Microsatellite genotype '
                                             'scores for a contemporary, range-wide sample of Santa Ana sucker in '
                                             'southern California", "edition": "", "geospatialDataPresentationForm": '
                                             '"", "publicationDate": "20170101"}',
                           'limitations': '',
                           'maintenanceAndUpdateFrequency': '',
                           'publisher': '',
                           'purpose': None,
                           'useConstraints': ' '}
                          )

    def test_set_waf_identification_information_failure_empty_identification_fields(self):
        package_dict = waf_harvest_utils.set_waf_identification_information({}, {})

        assert_dict_equal(package_dict,
                          {'beginningTimePeriodOfContent': '{"date": "", "time": ""}',
                           'endingTimePeriodOfContent': '{"date": "", "time": ""}',
                           'limitations': '',
                           'maintenanceAndUpdateFrequency': '',
                           'purpose': None,
                           'useConstraints': ' '})

    def test_set_waf_keywords_success_default_single_list_values(self):
        iso_values = {'keywords':
            [{
             'type': 'theme',
             'keyword':[
                'endangered species',
             ]}]
        }
        package_dict = waf_harvest_utils.set_waf_keywords({}, iso_values)

        assert_dict_equal(package_dict, {
            'themeKeywords': u'endangered species',
            'placeKeywords': u'',
            'stratumKeywords': u'',
            'temporalKeywords': u'',
            'taxonKeywords': u''
        })

    def test_set_waf_keywords_success_default_multi_list_values(self):
        iso_values = {'keywords':  [
          {
             'type': 'theme',
             'keyword':[
                'endangered species',
                'genetics',
                'fish'
             ]
          },
          {
             'type': 'theme',
             'keyword': [
                'metapopulation',
                'admixture',
                'dendritic network',
                'hybridization'
             ]
          },
          {
             'type': 'place',
             'keyword': [
                'Santa Ana',
                'San Gabriel',
                'Los Angeles',
                'Santa Clara River watersheds',
                'southern California'
             ]
          },
          {
                'type': 'stratum',
                'keyword': ['test stratum']
          },
          {
                'type': 'temporal',
                'keyword': ['test temporal']
          },
          {
                'type': 'taxon',
                'keyword': ['test taxon']
          }
        ],
        }
        package_dict = waf_harvest_utils.set_waf_keywords({}, iso_values)

        assert_dict_equal(package_dict, {
            'themeKeywords': u'endangered species, genetics, fish, metapopulation, admixture, dendritic network, '
                             'hybridization',
            'placeKeywords': u'Santa Ana, San Gabriel, Los Angeles, Santa Clara River watersheds, southern California',
            'stratumKeywords': u'test stratum',
            'temporalKeywords': u'test temporal',
            'taxonKeywords': u'test taxon'
        })

    def test_set_waf_keywords_success_empty_values(self):
        package_dict = waf_harvest_utils.set_waf_keywords({}, {})

        assert_dict_equal(package_dict, {
            'themeKeywords': u'',
            'placeKeywords': u'',
            'stratumKeywords': u'',
            'temporalKeywords': u'',
            'taxonKeywords': u''
        })

    def test_set_waf_geologic_information_success_empty_geo_fields(self):
        iso_values = {
            'geologic-age': [],
            'beginning-geologic-age': '',
            'ending-geologic-age': '',
            'beginning-geologic-citation': '',
            'geographic-extent-description': ''
        }
        package_dict = waf_harvest_utils.set_waf_geologic_information({}, iso_values)

        assert_dict_equal(package_dict, {})

    def test_set_waf_geologic_information_success_populated_geo_fields(self):
        iso_values = {
            'geologic-age': [{
                'geologic-time-scale': 'test',
                'geologic-age-estimate': 'test',
                'geologic-age-uncertainty': 'test',
                'geologic-age-explanation': 'test'
            }],
            'beginning-geologic-age': {
                'geologic-time-scale': 'test',
                'geologic-age-estimate': 'test',
                'geologic-age-uncertainty': 'test',
                'geologic-age-explanation': 'test'
            },
            'ending-geologic-age': {
                'geologic-time-scale': 'test',
                'geologic-age-estimate': 'test',
                'geologic-age-uncertainty': 'test',
                'geologic-age-explanation': 'test'
            },
            'geologic-citation': {
                'title': 'title',
                'origin': 'origin',
                'pubdate': 'publication date',
                'geoform': 'geoform',
                'sername': 'sername',
                'issue': 'issue',
                'onlink': 'onlink'
            },
            'geographic-extent-description': 'test'
        }
        package_dict = waf_harvest_utils.set_waf_geologic_information({}, iso_values)

        assert_dict_equal(package_dict, {
            'geologicAge': '[{\"geologicAgeEstimate\": \"test\", \"geologicAgeExplanation\": \"test\", '
                           '\"geologicAgeUncertainty\": \"test\", \"geologicTimeScale\": \"test\"}]',
            'beginningGeologicAge': '{\"geologicAgeEstimate\": \"test\", \"geologicAgeExplanation\": \"test\", '
                                       '\"geologicAgeUncertainty\": \"test\", \"geologicTimeScale\": \"test\"}',
            'endingGeologicAge': '{\"geologicAgeEstimate\": \"test\", \"geologicAgeExplanation\": \"test\", '
                                       '\"geologicAgeUncertainty\": \"test\", \"geologicTimeScale\": \"test\"}',
            'geologicCitation': '{\"originator\": \"origin\", \"title\": \"title\", \"onlineLinkage\": \"onlink\", '
                                '\"sername\": \"sername\", \"geospatialDataPresentationForm\": \"geoform\", '
                                '\"issue\": \"issue\", \"publicationDate\": \"publication date\"}',
            'geographicExtentDescription': 'test'
        }
                          )

    def test_set_waf_bounding_information_success_empty_bounding_values(self):
        package_dict = waf_harvest_utils.set_waf_bounding_information({}, {})

        assert_dict_equal(package_dict, {'boundingCoordinate': '{\"westBoundingCoordinate\": \"\", '
                                                                        '\"southBoundingCoordinate\": \"\", '
                                                                        '\"northBoundingCoordinate\": \"\", '
                                                                        '\"eastBoundingCoordinate\": \"\"}'})

    def test_set_waf_bounding_information_success_populated_bounding_values(self):
        iso_values = {
            'bbox': [{
                'west': '1',
                'east': '2',
                'north': '3',
                'south': '4'
            }],
            'bounding-altitude': [{
                'minimum-altitude': '10',
                'maximum-altitude': '0',
                'altitude-units': 'meters'
            }]
        }
        package_dict = waf_harvest_utils.set_waf_bounding_information({}, iso_values)

        assert_dict_equal(package_dict, {'boundingAltitudes': '{\"altitudeMinimum\": "10", '
                                                                       '\"altitudeDistanceUnits\": \"meters\", '
                                                                       '\"altitudeMaximum\": \"0\"}',
                                                  'boundingCoordinate': '{\"westBoundingCoordinate\": \"1\", '
                                                                        '\"southBoundingCoordinate\": \"4\", '
                                                                        '\"northBoundingCoordinate\": \"3\", '
                                                                        '\"eastBoundingCoordinate\": \"2\"}'})

    def test_set_waf_citations_success_empty_values(self):
        iso_values = {
            'classsys-citation': '',
            'idref-citation': ''
        }
        package_dict = waf_harvest_utils.set_waf_citations({}, iso_values)

        assert_dict_equal(package_dict, {})

    def test_set_waf_citations_success_populated_values(self):
        iso_values = {
            'classsys-citation': {'origin': 'test'},
            'idref-citation': {'origin': 'test'}
        }
        package_dict = waf_harvest_utils.set_waf_citations({}, iso_values)

        assert_dict_equal(package_dict, {
            'classSysCitation': '{\"originator\": \"test\"}',
            'idRefCitation': '{\"originator\": \"test\"}'
        })

    def test_set_waf_contacts_success_empty_values(self):
        package_dict = waf_harvest_utils.set_waf_contacts({}, {})

        assert_dict_equal(package_dict, {
            'distributorContact': '{\"email\": [\"\"], \"contactOrganization\": \"\", \"contactPosition\": \"\", '
                                  '\"contactPerson\": \"\", \"telephone\": [\"\"]}',
            'distributorContactAddress': '[]',
            'metadataContact': '{\"email\": [\"\"], \"contactOrganization\": \"\", \"contactPosition\": \"\", '
                               '\"contactPerson\": \"\", \"telephone\": [\"\"]}',
            'metadataContactAddress': '[]'
        })

    def test_set_waf_contacts_success_empty_contact_info(self):
        iso_values = {
            'distributor': [
                {
                    'contact-address': [{
                        'addrtype': 'NA',
                        'address': '123 ABC Road',
                        'city': 'New York',
                        'state': 'NY',
                        'postal': '12345',
                        'country': 'USA'
                    }],
                    'role': 'distributor',
                    'organisation-name': 'Testers',
                    'individual-name': 'ScienceBase',
                    'position-name': ''
                }
            ]
        }
        package_dict = waf_harvest_utils.set_waf_contacts({}, iso_values)

        assert_dict_equal(package_dict, {
            'distributorContact': '{\"email\": \"\", \"contactOrganization\": \"Testers\", \"contactPosition\": \"\", '
                                  '\"contactPerson\": \"ScienceBase\", \"telephone\": \"\"}',
            'distributorContactAddress': '[{\"city\": \"New York\", \"addressType\": \"NA\", \"country\": \"USA\",'
                                         ' \"state\": \"NY\", \"address\": \"123 ABC Road\", \"postalCode\": '
                                         '\"12345\"}]',
            'metadataContact': '{\"email\": [\"\"], \"contactOrganization\": \"\", \"contactPosition\": \"\", '
                               '\"contactPerson\": \"\", \"telephone\": [\"\"]}',
            'metadataContactAddress': '[]'
        })

    def test_set_waf_contacts_success_empty_contact_address(self):
        iso_values = {
            'distributor': [
                {
                    'contact-info': {
                        'online-resource': '',
                        'email': 'test@test.com'
                    },
                    'role': 'pointOfContact',
                    'organisation-name': 'Testers',
                                                'individual-name': 'Test Testingtono',
                    'position-name': ''
                }
            ]
        }
        package_dict = waf_harvest_utils.set_waf_contacts({}, iso_values)

        assert_dict_equal(package_dict, {
            'distributorContact': '{\"email\": \"test@test.com\", \"contactOrganization\": \"Testers\", '
                                  '\"contactPosition\": \"\", \"contactPerson\": \"Test Testingtono\", '
                                  '\"telephone\": \"\"}',
            'distributorContactAddress': '[]',
            'metadataContact': '{\"email\": [\"\"], \"contactOrganization\": \"\", \"contactPosition\": \"\", '
                               '\"contactPerson\": \"\", \"telephone\": [\"\"]}',
            'metadataContactAddress': '[]'
        })

    def test_set_waf_contacts_success_populated_values(self):
        iso_values = {
            'ider-contact': [
                {
                    'contact-info': {
                        'online-resource': '',
                        'email': 'test@test.com'
                    },
                    'contact-address': [{
                        'addrtype': 'NA',
                        'address': '123 ABC Road',
                        'city': 'New York',
                        'state': 'NY',
                        'postal': '12345',
                        'country': 'USA'
                    }],
                    'role': 'distributor',
                    'organisation-name': 'Testers',
                    'individual-name': 'Test Testington',
                    'position-name': ''
                }
            ],
            'vouchers-contact': [
                {
                    'contact-info': {
                        'online-resource': '',
                        'email': 'test@test.com'
                    },
                    'contact-address': [{
                        'addrtype': 'NA',
                        'address': '123 ABC Road',
                        'city': 'New York',
                        'state': 'NY',
                        'postal': '12345',
                        'country': 'USA'
                    }],
                    'role': 'distributor',
                    'organisation-name': 'Testers',
                    'individual-name': 'Test Testington',
                    'position-name': ''
                }
            ],
            'vouchers-specimen': 'Test',
            'distributor': [
                {
                    'contact-info': {
                        'online-resource': '',
                        'email': 'test@test.com'
                    },
                    'contact-address': [{
                        'addrtype': 'NA',
                        'address': '123 ABC Road',
                        'city': 'New York',
                        'state': 'NY',
                        'postal': '12345',
                        'country': 'USA'
                    }],
                    'role': 'distributor',
                    'organisation-name': 'Testers',
                    'individual-name': 'ScienceBase',
                    'position-name': ''
                }
            ],
            'metadata-point-of-contact': [
                {
                    'contact-info': {
                        'online-resource': '',
                        'email': 'test@test.com'
                    },
                    'contact-address': [{
                        'addrtype': 'NA',
                        'address': '123 ABC Road',
                        'city': 'New York',
                        'state': 'NY',
                        'postal': '12345',
                        'country': 'USA'
                    }],
                    'role': 'pointOfContact',
                    'organisation-name': 'Testers',
                                                'individual-name': 'Test Testingtono',
                    'position-name': ''
                }
            ]
        }
        package_dict = waf_harvest_utils.set_waf_contacts({}, iso_values)

        assert_dict_equal(package_dict, {
            'distributorContact': '{\"email\": \"test@test.com\", \"contactOrganization\": \"Testers\", '
                                  '\"contactPosition\": \"\", \"contactPerson\": \"ScienceBase\", \"telephone\": \"\"}',
            'distributorContactAddress': '[{\"city\": \"New York\", \"addressType\": \"NA\", \"country\": \"USA\", \"'
                                         'state\": \"NY\", \"address\": \"123 ABC Road\", \"postalCode\": \"12345\"}]',
            'iderContact': '{\"email\": \"test@test.com\", \"contactOrganization\": \"Testers\", \"contactPosition\": '
                           '\"\", \"contactPerson\": \"Test Testington\", \"telephone\": \"\"}',
            'iderContactAddress': '[{\"city\": \"New York\", \"addressType\": \"NA\", \"country\": \"USA\", \"state\": '
                                  '\"NY\", \"address\": \"123 ABC Road\", \"postalCode\": \"12345\"}]',
            'metadataContact': '{\"email\": \"test@test.com\", \"contactOrganization\": \"Testers\", \"contactPosition'
                               '\": \"\", \"contactPerson\": \"Test Testingtono\", \"telephone\": \"\"}',
            'metadataContactAddress': '[{\"city\": \"New York\", \"addressType\": \"NA\", \"country\": \"USA\", \"state'
                                      '\": \"NY\", \"address\": \"123 ABC Road\", \"postalCode\": \"12345\"}]',
            'vouchersContact': '{\"email\": \"test@test.com\", \"contactOrganization\": \"Testers\", \"contactPosition'
                               '\": \"\", \"contactPerson\": \"Test Testington\", \"telephone\": \"\"}',
            'vouchersContactAddress': '[{\"city\": \"New York\", \"addressType\": \"NA\", \"country\": \"USA\", '
                                      '\"state\": \"NY\", \"address\": \"123 ABC Road\", \"postalCode\": \"12345\"}]',
            'vouchersSpecimen': 'Test'
        })

    def test_set_waf_data_quality_information_success_empty_values(self):
        modified_package_dict = waf_harvest_utils.set_waf_data_quality_information({}, {})

        assert_dict_equal(modified_package_dict, {})

    def test_set_waf_data_quality_information_success_populated_values(self):
        iso_values = {
            'attribute-accuracy-report': 'Test',
            'completeness-report': 'Test',
            'lineage-citation': {
                'title': 'NA',
                'origin': 'NA',
                'pubdate': 'NA',
                'geoform': 'NA'
            },
            'source-scale-denominator': 'Test',
            'type-of-source-media': 'Test',
            'source-currentness-reference': 'Test',
            'source-citation-abbreviation': 'Test',
            'distribution-liability': 'Test'
        }
        package_dict = waf_harvest_utils.set_waf_data_quality_information({}, iso_values)

        assert_dict_equal(package_dict, {
            'attributeAccuracyReport': 'Test',
            'completenessReport': 'Test',
            'distributionLiability': 'Test',
            'lineageCitation': '{\"originator\": \"NA\", \"geospatialDataPresentationForm\": \"NA\", \"publicationDate'
                               '\": \"NA\", \"title\": \"NA\"}',
            'sourceCitationAbbreviation': 'Test',
            'sourceCurrentnessReference': 'Test',
            'sourceScaleDenominator': 'Test',
            'typeOfSourceMedia': 'Test'
        })

    def test_set_waf_spatial_reference_information_success_empty_values(self):
        package_dict = waf_harvest_utils.set_waf_spatial_reference_information({}, {})

        assert_dict_equal(package_dict, {})

    def test_set_waf_spatial_reference_information_success_populated_values(self):
        iso_values = {
            'map-projection-name': 'Test',
            'planar-coordinate-information': {
                'planar-coordinate-encoding-method': 'NA',
                'abscissa-resolution': 'NA',
                'ordinate-resolution': 'NA',
                'planar-distance-units': 'NA'
            },
            'horizontal-datum-name': 'Test'
        }
        package_dict = waf_harvest_utils.set_waf_spatial_reference_information({}, iso_values)

        assert_dict_equal(package_dict, {
            'horizontalDatumName': 'Test',
            'mapProjectionName': 'Test',
            'planarCoordinateInformation': '{\"planarCoordinateEncodingMethod\": \"NA\", \"ordinateResolution\": \"NA\"'
                                           ', \"planarDistanceUnits\": \"NA\", \"abscissaResolution\": \"NA\"}'
        })

    def test_set_metadata_reference_information_success_empty_values(self):
        package_dict = waf_harvest_utils.set_metadata_reference_information({}, {})

        assert_dict_equal(package_dict, {})
