import json
import os

import ckanext.cnra_schema.helpers as cnra_schema_helpers
from nose.tools import assert_raises, assert_equal, assert_dict_equal, assert_list_equal, assert_false

fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')


def get_iso_values():
    with open(os.path.join(fixtures_path, 'iso_values.json'), 'r') as f:
        result = json.load(f)
    return result


def get_modified_iso_values():
    with open(os.path.join(fixtures_path, 'iso_values_without_harvest_job_config_values.json'), 'r') as f:
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
    with open(os.path.join(fixtures_path, 'expected_extras_package_dict.json'), 'r') as f:
        result = json.load(f)
    return result


class TestHelperFunctions(object):

    assert_list_equal.__self__.maxDiff = None
    assert_dict_equal.__self__.maxDiff = None

    harvest_job_config = get_harvest_job_config()
    iso_values = get_iso_values()
    modified_iso_values = get_modified_iso_values()

    def test_delete_from_extras_success(self):
        package_dict = get_package_dict()
        key = 'progress'

        expected_modified_package_dict = get_expected_modified_package_dict()
        del expected_modified_package_dict.get('extras')[16]
        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), expected_modified_package_dict.get('extras'))


    def test_delete_from_extras_failure(self):
        package_dict = get_package_dict()
        key = 'backup_contact_email'

        expected_modified_package_dict = get_expected_modified_package_dict()
        cnra_schema_helpers.delete_existing_extra_from_package_dict(key, package_dict)

        assert_list_equal(package_dict.get('extras'), expected_modified_package_dict.get('extras'))


    def test_set_waf_map_fields_from_source_values(self):
        package_dict = get_package_dict()
        map_fields = self.harvest_job_config.get('map_fields', {})
        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, self.iso_values,
                                                                             map_fields)

        for map_field in map_fields:
            target_field = map_field.get('target')
            source_field = map_field.get('source')
            iso_source_field = self.iso_values.get(source_field)

            if isinstance(iso_source_field, list):
                iso_source_field = ', '.join(str(x) for x in iso_source_field)

            assert_equal(iso_source_field, modified_package_dict.get(target_field))


    def test_set_waf_map_fields_from_default_values(self):
        package_dict = get_package_dict()
        map_fields = self.harvest_job_config.get('map_fields', {})
        modified_package_dict = cnra_schema_helpers.set_waf_map_fields(package_dict, self.modified_iso_values,
                                                                             map_fields)

        for map_field in map_fields:
            target_field = map_field.get('target')
            default_field = map_field.get('default')

            if isinstance(target_field, list):
                target_field = ', '.join(str(x) for x in target_field)

            assert_equal(default_field, modified_package_dict.get(target_field))


    def test_set_waf_publisher_values_from_iso_values(self):
        package_dict = get_package_dict()
        publisher_mapping = self.harvest_job_config.get('publisher', {})
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(package_dict, self.iso_values, publisher_mapping)

        assert_equal(self.iso_values.get('publisher'), modified_package_dict.get('publisher'))


    def test_set_waf_publisher_values_from_harvest_job_config(self):
        package_dict = get_package_dict()
        publisher_mapping = self.harvest_job_config.get('publisher', {})
        modified_package_dict = cnra_schema_helpers.set_waf_publisher_values(package_dict, self.modified_iso_values,
                                                                             publisher_mapping)

        assert_equal(publisher_mapping.get('default_publisher'), modified_package_dict.get('publisher'))


    def test_set_waf_contact_point_from_iso_values(self):
        package_dict = get_package_dict()
        contact_point_mapping = self.harvest_job_config.get('contact_point', {})
        name_field = contact_point_mapping.get('name_field')
        email_field = contact_point_mapping.get('email_field')
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(package_dict, self.iso_values,
                                                                          contact_point_mapping)

        iso_values_contact_name = self.iso_values.get('contact')
        iso_values_contact_email = self.iso_values.get('contact-email')

        assert_equal(iso_values_contact_name, modified_package_dict.get(name_field))
        assert_equal(iso_values_contact_email, modified_package_dict.get(email_field))


    def test_set_waf_contact_point_from_default_values(self):
        package_dict = get_package_dict()
        contact_point_mapping = self.harvest_job_config.get('contact_point', {})
        name_field = contact_point_mapping.get('name_field')
        email_field = contact_point_mapping.get('email_field')
        modified_package_dict = cnra_schema_helpers.set_waf_contact_point(package_dict, self.modified_iso_values,
                                                                          contact_point_mapping)

        default_values_contact_name = contact_point_mapping.get('default_name')
        default_values_contact_email = contact_point_mapping.get('default_email')

        assert_equal(default_values_contact_name, modified_package_dict.get(name_field))
        assert_equal(default_values_contact_email, modified_package_dict.get(email_field))