import json
import os

import ckanext.cnra_schema.helpers as cnra_schema_helpers
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false


class TestHelperFunctions(object):

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
