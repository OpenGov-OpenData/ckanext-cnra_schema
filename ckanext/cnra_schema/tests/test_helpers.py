import json
import os

import ckanext.cnra_schema.helpers as cnra_schema_helpers
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal

fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')


def get_iso_values():
    with open(os.path.join(fixtures_path, 'iso_values.json'), 'r') as f:
        result = json.load(f)
    return result


def get_harvest_job_config():
    with open(os.path.join(fixtures_path, 'harvest_job_config.json'), 'r') as f:
        result = json.load(f)
    return result


def get_package_dict():
    with open(os.path.join(fixtures_path, 'package_dict.json'), 'r') as f:
        result = json.load(f)
    return result


def get_expected_modified_package_dict():
    with open(os.path.join(fixtures_path, 'expected_modified_package_dict.json'), 'r') as f:
        result = json.load(f)
    return result


class TestHelperFunctions:

    package_dict = get_package_dict()
    harvest_job_config = get_harvest_job_config()
    iso_values = get_iso_values()

    def test_get_extra_success(self):
        expected_extras = self.package_dict.get('extras').get('bbox-south-lat')
        extras = cnra_schema_helpers.get_extra('bbox-south-lat', self.package_dict)

        assert_equal(expected_extras, extras)

    def test_get_extra_failure(self):
        expected_extras = self.package_dict.get('extras').get('secrets_of_the_universe')
        extras = cnra_schema_helpers.get_extra('secrets_of_the_universe', self.package_dict)

        assert_equal(expected_extras, extras)

    def test_set_waf_map_fields_success(self):
        map_fields = self.harvest_job_config.get('map_fields', {})
        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(self.package_dict, self.iso_values
                                                                       , map_fields)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop("publisher")
        expected_modified_package_dict.pop("contact_name")
        expected_modified_package_dict.pop("contact_email")

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)

    def test_set_waf_map_fields_failure(self):
        modified_harvest_job_config = self.harvest_job_config
        modified_harvest_job_config.pop("map_fields")
        contact_point_mapping = modified_harvest_job_config.get('map_fields', {})
        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(self.package_dict, self.iso_values
                                                                       , contact_point_mapping)
        modified_package_dict.get('extras').remove(16)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop('spatial_coverage')
        expected_modified_package_dict.pop('language')
        expected_modified_package_dict.pop("publisher")
        expected_modified_package_dict.pop("contact_email")
        expected_modified_package_dict.pop('progress')
        expected_modified_package_dict.pop("contact_name")

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)

    def test_set_waf_publisher_values_success(self):
        publisher_mapping = self.harvest_job_config.get('publisher', {})
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(self.package_dict, self.iso_values,
                                                                             publisher_mapping)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop('spatial_coverage')
        expected_modified_package_dict.pop('language')
        expected_modified_package_dict.pop("contact_email")
        expected_modified_package_dict.pop('progress')
        expected_modified_package_dict.pop("contact_name")

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)

    def test_set_waf_publisher_values_failure(self):
        modified_harvest_job_config = self.harvest_job_config
        modified_harvest_job_config.pop("publisher")
        publisher_mapping = modified_harvest_job_config.get('publisher', {})
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(self.package_dict, self.iso_values,
                                                                             publisher_mapping)
        modified_package_dict.get('extras').remove(16)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop('spatial_coverage')
        expected_modified_package_dict.pop('language')
        expected_modified_package_dict.pop("publisher")
        expected_modified_package_dict.pop("contact_email")
        expected_modified_package_dict.pop('progress')
        expected_modified_package_dict.pop("contact_name")

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)

    def test_set_waf_contact_point_success(self):
        contact_point_mapping = self.harvest_job_config.get('contact_point', {})
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(self.package_dict, self.iso_values,
                                                                          contact_point_mapping)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop('spatial_coverage')
        expected_modified_package_dict.pop('language')
        expected_modified_package_dict.pop("publisher")
        expected_modified_package_dict.pop('progress')

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)

    def test_set_waf_contact_point_failure(self):
        modified_harvest_job_config = self.harvest_job_config
        modified_harvest_job_config.pop("contact_point")
        contact_point_mapping = modified_harvest_job_config.get('contact_point', {})
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(self.package_dict, self.iso_values,
                                                                          contact_point_mapping)
        modified_package_dict.get('extras').remove(16)
        expected_modified_package_dict = get_expected_modified_package_dict()
        expected_modified_package_dict.pop('spatial_coverage')
        expected_modified_package_dict.pop('language')
        expected_modified_package_dict.pop("publisher")
        expected_modified_package_dict.pop("contact_email")
        expected_modified_package_dict.pop('progress')
        expected_modified_package_dict.pop("contact_name")

        assert_dict_equal(expected_modified_package_dict, modified_package_dict)