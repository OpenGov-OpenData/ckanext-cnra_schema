import json
import os

import ckanext.cnra_schema.helpers as cnra_schema_helpers
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false


class TestHelperFunctions(object):

    def test_delete_from_extras_success(self):
        package_dict = {'extras': [{'value':'x', 'key':'progress'}]}
        key = 'progress'

        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [])


    def test_delete_from_extras_only_removes_key(self):
        package_dict = {'extras': [{'value': 'x', 'key': 'progress'},{'value': 'y', 'key': 'new_key'}]}
        key = 'progress'

        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [{'value': 'y', 'key': 'new_key'}])

    def test_delete_from_extras_failure(self):
        package_dict = {'extras': [{'value': 'x', 'key': 'progress'}]}
        key = 'backup_contact_email'

        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), [{'value': 'x', 'key': 'progress'}])

    def test_delete_from_extras_missing_extras_fields(self):
        package_dict = {}
        key = 'backup_contact_email'

        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_dict_equal(package_dict, {})


    def test_set_waf_map_fields_from_source_values(self):
        package_dict = {}
        map_fields = [{
            'default': 'English',
            'source':'language',
            'target': 'language'
        }]
        iso_values = {'language': 'Spanish'}


        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, iso_values,
                                                                             map_fields)

        assert_equal('Spanish', modified_package_dict.get('language'))


    def test_set_waf_map_fields_from_default_values(self):
        package_dict = {}
        map_fields = [{
            'default': 'English',
            'source': 'language',
            'target': 'language'
        }]
        iso_values = {}

        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, iso_values,
                                                                             map_fields)

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

        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)

        assert_dict_equal({'language':'English', 'spatial_coverage':'Canada'}, modified_package_dict)


    def test_set_waf_map_fields_value_is_list(self):
        package_dict = {}
        map_fields = [{
            'default': '00',
            'source': 'coordinate',
            'target': 'coordinate'
        }]
        iso_values = {'coordinate':['-75.57563781738281','-69.82928466796875']}

        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)

        assert_equal('-75.57563781738281, -69.82928466796875', modified_package_dict.get('coordinate'))


    def test_set_waf_map_fields_empty_map_field(self):
        package_dict = {}
        map_fields = []
        iso_values = {}
        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, iso_values,
                                                                       map_fields)

        assert_dict_equal({}, package_dict)


    def test_set_waf_publisher_values_from_iso_values(self):
        package_dict = {}
        publisher_mapping = {'publisher_field':'publisher', 'default_publisher':'Default-Publisher'}
        iso_values = {'publisher':'Test-User'}
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(package_dict, iso_values, publisher_mapping)

        assert_equal('Test-User', modified_package_dict.get('publisher'))


    def test_set_waf_publisher_values_from_harvest_job_config(self):
        package_dict = {}
        publisher_mapping = {'publisher_field':'publisher', 'default_publisher':'Default-Publisher'}
        iso_values = {}
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(package_dict, iso_values,
                                                                             publisher_mapping)

        assert_equal('Default-Publisher', modified_package_dict.get('publisher'))


    def test_set_waf_publisher_values_empty_publisher_mapping(self):
        package_dict = {}
        publisher_mapping = {}
        iso_values = {}
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(package_dict, iso_values,
                                                                             publisher_mapping)

        assert_dict_equal({}, package_dict)


    def test_set_waf_contact_point_from_iso_values(self):
        package_dict = {}
        contact_point_mapping = {
            'default_email':'test@default.com',
            'name_field':'contact_name',
            'default_name':'Default Name',
            'email_field':'contact_email'
        }
        iso_values = {'contact':'John Smith', 'contact-email':'test@test.com'}
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)


        assert_dict_equal({'contact_name':'John Smith', 'contact_email':'test@test.com'}, package_dict)


    def test_set_waf_contact_point_from_default_values(self):
        package_dict = {}
        contact_point_mapping = {
            'default_email': 'test@default.com',
            'name_field': 'contact_name',
            'default_name': 'Default Name',
            'email_field': 'contact_email'
        }
        iso_values = {}
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)

        assert_equal({'contact_name':'Default Name', 'contact_email':'test@default.com'}, package_dict)


    def test_set_waf_contact_point_empty_mapping(self):
        package_dict = {}
        contact_point_mapping = {}
        iso_values = {}
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(package_dict, iso_values,
                                                                          contact_point_mapping)

        assert_dict_equal({}, package_dict)

    def test_is_composite_field_populated_success_preset_composite(self):
        result = cnra_schema_helpers.is_composite_field_populated(
            {'sub_dict': "{'a': '1'}"}, {'field_name': 'sub_dict', 'preset': 'composite'})

        assert result

    def test_is_composite_field_populated_success_preset_composite_repeating(self):
        result = cnra_schema_helpers.is_composite_field_populated(
            {'sub_dict': "{'a': '1'}"}, {'field_name': 'sub_dict', 'preset': 'composite-repeating'})

        assert result

    def test_is_composite_field_populated_success_field_name_spatial_details(self):
        result = cnra_schema_helpers.is_composite_field_populated(
            {}, {'field_name': 'spatial_details', 'preset': 'composite'})

        assert result

    def test_is_composite_field_populated_failure_empty_field_in_package_dict(self):
        result = cnra_schema_helpers.is_composite_field_populated(
            {'sub_dict': "{'a': ''}"}, {'field_name': 'sub_dict', 'preset': 'composite'})

        assert not result

    def test_is_dict_populated_success_populated_simple_field_dict(self):
        result = cnra_schema_helpers.is_dict_populated({'sub_dict': "{'a': '1'}"})

        assert result

    def test_is_dict_populated_success_populated_multi_field_dict(self):
        result = cnra_schema_helpers.is_dict_populated({'sub_dict': "{'a': '', 'b: '2'}"})

        assert result

    def test_is_dict_populated_failure_populated_field_is_empty_dict(self):
        result = cnra_schema_helpers.is_dict_populated({})

        assert not result

    def test_is_dict_populated_failure_populated_field_is_empty_valued_dict(self):
        result = cnra_schema_helpers.is_dict_populated({'a': '', 'b': ''})

        assert not result

    def test_is_dict_populated_failure_populated_field_is_empty_list(self):
        result = cnra_schema_helpers.is_dict_populated([])

        assert not result

    def test_is_dict_populated_failure_populated_field_is_list_of_empty_stings(self):
        result = cnra_schema_helpers.is_dict_populated(['', '', ''])

        assert not result

    def test_is_dict_populated_failure_populated_field_is_list_of_empty_stings(self):
        result = cnra_schema_helpers.is_dict_populated(['', '', 'a'])

        assert result

    def test_is_dict_populated_failure_populated_field_is_list_of_empty_dict(self):
        result = cnra_schema_helpers.is_dict_populated([{'a': ''}])

        assert not result

    def test_is_dict_populated_failure_populated_field_is_list_of_empty_dicts(self):
        result = cnra_schema_helpers.is_dict_populated([{'a': ''}, {'b': ''}])

        assert not result

    def test_is_dict_populated_success_populated_field_is_list_of_populate_dicts(self):
        result = cnra_schema_helpers.is_dict_populated([{'a': ''}, {'b': '2'}])

        assert result

    def test_is_dict_populated_failure_populated_field_is_dict_with_empty_list(self):
        result = cnra_schema_helpers.is_dict_populated({'originator': []})

        assert not result

    def test_is_dict_populated_failure_populated_field_is_dict_with_empty_dict_with_list_of_stings(self):
        result = cnra_schema_helpers.is_dict_populated({'originator': ['', '', '']})

        assert not result

    def test_is_dict_populated_success_populated_field_is_list_of_dicts(self):
        result = cnra_schema_helpers.is_dict_populated({'ab': [{'a': '1'}, {'b': '2'}]})

        assert result

    def test_is_dict_populated_success_populated_field_is_dict_of_mixed_empty_values(self):
        result = cnra_schema_helpers.is_dict_populated({'originator': ['', '', ''], 'title': '',
                                                        'onlineLinkage': ['', ''], 'sername': '',
                                                        'geospatialDataPresentationForm': '', 'issue': '',
                                                        'publicationDate': ''})

        assert not result

    def test_is_dict_populated_success_populated_field_is_dict_of_mixed_values_one_populated(self):
        result = cnra_schema_helpers.is_dict_populated({'originator': ['', '', ''], 'title': '',
                                                        'onlineLinkage': ['', ''], 'sername': '',
                                                        'geospatialDataPresentationForm': '', 'issue': '',
                                                        'publicationDate': '2020-12-25'})

        assert result
